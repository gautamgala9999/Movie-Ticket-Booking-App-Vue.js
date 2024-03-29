from datetime import datetime
import datetime
from flask import Flask,  request, jsonify, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user,  login_user,   UserMixin, LoginManager
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from functools import wraps
import csv, io
import redis
from worker import celery_app
from celery.schedules import crontab

app = Flask(__name__)   
cel = celery_app

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
app.secret_key = 'ticket_booking_website'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.app_context().push()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app, origins=["http://localhost:3000"])

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

celery_app.conf.beat_schedule = {
    'show_stats_monthly': {
        'task': 'tasks.show_stats_monthly', 
        'schedule': crontab(minute=0, hour=0, day_of_month=1),  
    },
    'daily_reminders': {
        'task': 'tasks.daily_reminders',  
        'schedule': crontab(minute=0, hour=18), 
    },
}

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    rating = db.Column(db.String(25))
    tag = db.Column(db.String(75))
    datetime = db.Column(db.String(75), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    # shows = db.relationship('Ticket')
    def __init__(self, name, description, rating, tag, datetime, venue_id):
        self.name = name
        self.description = description
        self.rating = rating
        self.tag = tag
        self.datetime = datetime
        self.venue_id = venue_id

    def __repr__(self):
        return f"Show(id={self.id}, name='{self.name}',datetime='{self.datetime}', venue_id={self.venue_id})"

    def __str__(self):
        return self.name


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rating': self.rating,
            'tag': self.tag,
            'datetime': self.datetime,
            'venue_id': self.venue_id
        }
    

class Venue(db.Model): 
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    def __init__(self, name, location, capacity):
        self.name = name
        self.location = location
        self.capacity = capacity

    def __repr__(self):
        return f"Venue(id={self.id}, name='{self.name}, location={self.location}, capacity= {self.capacity}')"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'capacity': self.capacity
        }
    

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(255),default='user')
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}, role={self.role}')"

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}, role={self.role})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
 
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    date_purchased = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Kolkata')))
    def __init__(self, user_id, show_id, date_purchased=None):
        self.user_id = user_id
        self.show_id = show_id
        self.date_purchased = date_purchased or datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    def __repr__(self):
        return f"Ticket(id={self.id}, user_id={self.user_id}, show_id={self.show_id})"

    def __str__(self):
        return f"Ticket for Show ID: {self.show_id}"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'date_purchased': self.date_purchased.isoformat()
        }

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data 
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args,**kwargs)

    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():    

    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        payload = {
            'email_id': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1) 
        }
        if user:
            if user.password == password:
                print(user.role)
                login_user(user, remember=True)
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                print(token)

                return jsonify({'token': token,"message": "User logged in successfully", "user_id": user.id,"user_name":user.name, "role":user.role}), 200
                # return jsonify({"message": "User logged in successfully", "user_id": user.id,"user_name":user.name, "role":user.role}), 200
            else:
                return jsonify({"error": "Invalid password"}), 400
        else:
            return jsonify({"error": "Invalid email"}), 400
        
    return jsonify({"error": "Invalid request"}), 400


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.get_json())
        data = request.get_json()
        name = data['name']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        if len(name) < 3: 
            return jsonify({"error": "Name must be greater than 2 characters."}), 400
        elif len(email) < 6: 
            return jsonify({"error": "Email must be greater than 5 characters."}), 400
        elif len(password1) < 7: 
            return jsonify({"error": "Password must be at least 7 characters."}), 400
        elif password1 != password2:
            return jsonify({"error": "Passwords don't match."}), 400
        else:
            new_user = User(name=name, email=email, password=password1) 
            db.session.add(new_user)
            db.session.commit()
            print('Successfully signed up.')
        
    return jsonify({"message": "User created successfully"}), 200

@app.route('/search', methods=['GET'])
def search():
    input = request.args.get('input')
    show_results = []
    venue_results = []
    result_type=""
    results=[]
    if input:
        show_results = Show.query.filter(Show.name.ilike(f"%{input}%")).all()
    
        show_results += Show.query.filter(Show.rating == input).all()
    
        show_results += Show.query.filter(Show.tag.ilike(f"%{input}%")).all()
    
        show_results += Show.query.filter(Show.description.ilike(f"%{input}%")).all()

        venue_results = Venue.query.filter(Venue.name.ilike(f"%{input}%")).all()

        venue_results += Venue.query.filter(Venue.location.ilike(f"%{input}%")).all()
    
    if show_results and not venue_results:
        result_type = "Show"
        results = [show.to_dict() for show in show_results]
    elif venue_results and not show_results:
        result_type = "Venue"
        results = [venue.to_dict() for venue in venue_results]
    elif not show_results and not venue_results:
        result_type=""
        results=[]
    elif  show_results and  venue_results:
        result_type = "Mixed"
        results = {
            "shows": [show.to_dict() for show in show_results],
            "venues": [venue.to_dict() for venue in venue_results]
        }
    
    return jsonify({"result_type": result_type, "results": results})


@app.route('/create_shows', methods=['POST'])
@token_required
def create_shows():

    try:
        if request.method == 'POST':
            data = request.get_json()
            name = data['name']
            description = data['description']
            rating = data['rating']
            tag = data['tag']
            datetime = data['datetime']
            venue_id = data['venue_id']
            if name is None or description is None or rating is None or tag is None or venue_id is None:
                return jsonify({"error": "Missing required data"}), 400
            
            new_show = Show(name=name, description=description, rating=rating, tag=tag, datetime=datetime, venue_id=venue_id)
            redis_client.delete('show_shows')
            db.session.add(new_show)
            db.session.commit()

            return jsonify({"message": "Show created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# NON REDIS IMPLEMENTED FUNCTION
# @app.route('/show_shows', methods=['GET', 'POST'])
# def show_shows():
#     shows=Show.query.all()
#     show_dicts = [show.to_dict() for show in shows]    
#     return jsonify(show_dicts)


# REDIS IMPLEMENTED FUNCTION
@app.route('/show_shows', methods=['GET', 'POST'])
def show_shows():
    cached_data = redis_client.get('show_shows')
    if cached_data:
        return cached_data.decode('utf-8')
    else:
        shows = Show.query.all()
        show_dicts = [show.to_dict() for show in shows]
        json_data = jsonify(show_dicts).get_data()
        redis_client.setex('show_shows', 30, json_data)

        return json_data


@app.route('/show_shows/<int:show_id>', methods=['GET', 'POST'])
def show_show(show_id):
    show = Show.query.get(show_id)
    show_dicts = show.to_dict()
    return jsonify(show_dicts)

@app.route('/update_shows/<int:show_id>', methods=['POST','GET'])
@token_required
def update_shows(show_id):
    try:
        data = request.get_json()
        print(request.get_json())
        name = data['name']
        description = data['description']
        rating = data['rating']
        tag = data['tag']
        datetime_value = data['datetime']
	
        if name is None or description is None or rating is None or tag is None or datetime_value is None:
            return jsonify({"error": "Missing required data"}), 400


        this_show = Show.query.get(show_id)
        if this_show:
            this_show.name = name
            this_show.description = description
            this_show.rating = rating
            this_show.tag = tag
            this_show.datetime = datetime_value
            redis_client.delete('show_shows')

            db.session.commit()
            return jsonify({"message": "Show updated successfully"}), 200
        else:
            return jsonify({"error": "Show not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_shows/<int:show_id>', methods=['POST','GET'])
def delete_shows(show_id):
    try:
        this_show = Show.query.get(show_id)
        if this_show:
            redis_client.delete('show_shows')
            db.session.delete(this_show)
            db.session.commit()
            return jsonify({"message": "Show deleted successfully"}), 200
        else:
            return jsonify({"error": "Show not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/create_venue', methods=['POST'])
@token_required
def create_venue():
    try:
        data = request.get_json()
        name = data.get('name')
        location = data.get('location')
        capacity = data.get('capacity')

        if name is None or location is None or capacity is None:
            return jsonify({"error": "Missing required data"}), 400

        new_venue = Venue(name=name, location=location, capacity=capacity)
        redis_client.delete('show_venue')
        db.session.add(new_venue)
        db.session.commit()

        return jsonify({"message": "Venue created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# NON REDIS IMPLEMENTED FUNCTION
# @app.route('/show_venue', methods=['GET', 'POST'])
# def show_venue():
#     venues=Venue.query.all()
#     venue_dict = [venue.to_dict() for venue in venues]
#     return jsonify(venue_dict)


# REDIS IMPLEMENTED FUNCTION
@app.route('/show_venue', methods=['GET', 'POST'])
def show_venue():
    cached_data = redis_client.get('show_venue')
    if cached_data:
        return cached_data.decode('utf-8')
    else:
        venues = Venue.query.all()
        venue_dicts = [venue.to_dict() for venue in venues]
        json_data = jsonify(venue_dicts).get_data()
        redis_client.setex('show_venue', 30, json_data)

        return json_data


@app.route('/show_venue/<int:venue_id>',methods=['GET','POST'])
def show_venue1(venue_id):
    venue=Venue.query.get(venue_id)
    venue_dicts= venue.to_dict()
    return jsonify(venue_dicts)

@app.route('/update_venue/<int:venue_id>', methods=['POST','GET'])
@token_required
def update_venue(venue_id):
    try:
        this_venue = Venue.query.get(venue_id)
        print(this_venue)
        if this_venue:
            data = request.get_json()
            print(request.get_json())
            name = data['name']
            location = data['location']
            capacity = data['capacity']

            if name is None or location is None or capacity is None:
                return jsonify({"error": "Missing required data"}), 400

            this_venue.name = name
            this_venue.location = location
            this_venue.capacity = capacity
            redis_client.delete('show_venue')

            db.session.commit()
            return jsonify({"message": "Venue updated successfully"}), 200
        else:
            return jsonify({"error": "Venue not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_venue/<int:venue_id>', methods=['POST','GET'])
def delete_venue(venue_id):
    try:
        this_venue = Venue.query.get(venue_id)
        if this_venue:
            redis_client.delete('show_venue')
            db.session.delete(this_venue)
            db.session.commit()
            return jsonify({"message": "Venue deleted successfully"}), 200
        else:
            return jsonify({"error": "Venue not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/book_tickets/<int:show_id>', methods=['GET', 'POST'])
@token_required
def book_tickets(show_id):   
    try:
        # print('inside')
        show = Show.query.get(show_id)
        if not show:
            return jsonify({'error': 'Invalid show ID'}), 404
        
        if request.method == 'GET':
            show = Show.query.get(show_id)
            show_toDict = show.to_dict()
            return jsonify(show_toDict)

        if request.method == 'POST':
            venue = Venue.query.get(show.venue_id)
            print(venue.capacity)
            if not venue:
                return jsonify({'error': 'Venue not found'}), 404
            
            tickets = int(request.json['numTickets'])
            email = request.json['email']
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
        
            if tickets > venue.capacity:
                 return jsonify({'error': 'Not enough tickets available'}), 400
            
            
            venue.capacity -= tickets
            list_tickets = []
            for _ in range(tickets):
                ticket = Ticket(show_id=show_id, user_id=user.id)
                list_tickets.append(ticket)
                db.session.add(ticket)
            # print('side')
            redis_client.delete('bookings')
            db.session.commit()
            return jsonify({'message': 'Tickets booked successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/csv_shows', methods=['GET', 'POST'])
def csv_shows():
    shows_data = Show.query.all()  
    shows_dicts = []
    
    for show in shows_data:
        show_dict = {
            'id': show.id,
            'name': show.name, 
            'description': show.description, 
            'rating': show.rating, 
            'tag': show.tag, 
            'datetime': show.datetime, 
            'venue_id': show.venue_id 
        }
        shows_dicts.append(show_dict)
    # print(shows_dicts)
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=["id", "name", "description", "rating", "tag", "datetime", "venue_id"])
    csv_writer.writeheader()
    csv_writer.writerows(shows_dicts)
    output.seek(0)
    
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=shows.csv"})


@app.route('/csv_venue', methods=['GET', 'POST'])
def csv_venue():
    venues_data = Venue.query.all()
    venues_dicts = []
    for venue in venues_data:
        venue_dict = {
            "id" : venue.id,
            "name": venue.name,
            "location": venue.location,
            "capacity": venue.capacity
        }
        venues_dicts.append(venue_dict)
    # print(venues_dicts)
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=["id","name", "location", "capacity"])
    csv_writer.writeheader()
    csv_writer.writerows(venues_dicts)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=venues.csv"})

    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        this_user_id=current_user.id 
        num_tickets=Ticket.query.filter(Ticket.user_id==this_user_id).all()
        num_tickets=reversed(num_tickets)
        ticket_data = [{'id': ticket.id, 'user_id': ticket.user_id, 'show_id':ticket.show_id} for ticket in num_tickets]
        print(ticket_data)
        return jsonify({
            'user_id': this_user_id,
            'num_tickets': ticket_data
        })
    except:
        return jsonify({'error': 'An error occurred'})
    
# NON REDIS IMPLEMENTED FUNCTION
# @app.route('/bookings', methods=['GET'])
# def bookings():
#     try:
#         tickets = Ticket.query.all()
#         print(tickets)
#         ticket_data = [ticket.to_dict() for ticket in (tickets)]
#         return jsonify({'ticket_data': ticket_data})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# REDIS IMPLEMENTED FUNCTION
@app.route('/bookings', methods=['GET'])
def bookings():
    try:
        cached_data = redis_client.get('bookings')
        if cached_data:
            return cached_data.decode('utf-8')
        else:
            tickets = Ticket.query.all()
            ticket_data = [ticket.to_dict() for ticket in tickets]
            json_data = jsonify({'ticket_data': ticket_data}).get_data()
            redis_client.setex('bookings', 30, json_data)
            return json_data
    except Exception as e:
        return jsonify({'error': str(e)})

import tasks

def cel_jobs():
    # adda_result = tasks.add.delay()
    daily=tasks.daily_reminders.delay()
    monthly=tasks.show_stats_monthly.delay()
    return ''
    # from datetime import datetime
    # import pytz
    # oho= (datetime.now(pytz.timezone('Asia/Kolkata')))
    # return f"Result: {adda_result.id}<br>Result Daily: {daily.id}<br>Result Monthly: {monthly.id}<br>--{oho}--"

if __name__=='__main__':
    db.create_all()
    # cel_jobs()
    app.run(debug=True, port = 8000)

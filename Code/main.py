from datetime import datetime
import datetime
from flask import Flask,  request, jsonify, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, logout_user, LoginManager, UserMixin
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery
import jwt
from functools import wraps
import csv, io

app = Flask(__name__)
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

# Celery configuration      
celery = Celery(
    'myapp',
    broker='redis://localhost:6379/0',  # Replace with your broker URL
    include=__name__
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

class Show(db.Model):# type: ignore
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
    

class Venue(db.Model): # type: ignore
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
    

class User(UserMixin, db.Model):# type: ignore
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
 
class Ticket(db.Model):# type: ignore
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

tshows=Show.query.all()
tvenues=Venue.query.all()
tall=tshows+(tvenues)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if the 'Authorization' header is present
        # print(request.headers)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verify the token using the secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data  # This can be used to access user data in your route functions
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args,**kwargs)

    return decorated


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     tshows=Show.query.all()
#     tvenues=Venue.query.all()
#     tall=tshows+(tvenues)
#     tall_dicts = [item.to_dict() for item in tall]
#     return render_template("home.html", user=current_user ,tall=tall_dicts)
#     # return jsonify(tall=tall_dicts)

# @app.route('/login/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         if email=='admin@domain.com' and password=='admin@123':
#             return render_template('admin_login.html',user=current_user ,tall=tall)
#     return render_template('admin.html',user=current_user ,tall=tall)


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

                return jsonify({'token': token,"message": "User logged in successfully", "user_id": user.id,"user_name":user.name, "role":user.role}), 201
                # return jsonify({"message": "User logged in successfully", "user_id": user.id,"user_name":user.name, "role":user.role}), 201
            else:
                return jsonify({"error": "Invalid password"}), 400
        else:
            return jsonify({"error": "Invalid email"}), 400
        
    return jsonify({"error": "Invalid request"}), 400



# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     logout_user()
#     print('You have logged out.')
#     return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.get_json())
        data = request.get_json()
        name = data['name']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        if len(name) < 3: # type: ignore
            return jsonify({"error": "Name must be greater than 2 characters."}), 400
        elif len(email) < 6: # type: ignore
            return jsonify({"error": "Email must be greater than 5 characters."}), 400
        elif len(password1) < 7: # type: ignore
            return jsonify({"error": "Password must be at least 7 characters."}), 400
        elif password1 != password2:
            return jsonify({"error": "Passwords don't match."}), 400
        else:
            new_user = User(name=name, email=email, password=password1) # type: ignore
            db.session.add(new_user)
            db.session.commit()
            print('Successfully signed up.')
        
    return jsonify({"message": "User created successfully"}), 201

@app.route('/search', methods=['GET'])
def search():
    # Get query parameters from the request
    name = request.args.get('name')
    rating = request.args.get('rating')
    tag = request.args.get('tag')
    desc = request.args.get('desc')
    loc = request.args.get('loc')
    
    # Initialize empty lists for show and venue results
    show_results = []
    venue_results = []
    
    # Search for shows
    if name:
        show_results = Show.query.filter(Show.name.ilike(f"%{name}%")).all()
    if rating:
        show_results = Show.query.filter(Show.rating == rating).all()
    if tag:
        show_results = Show.query.filter(Show.tag.ilike(f"%{tag}%")).all()
    if desc:
        show_results += Show.query.filter(Show.description.ilike(f"%{desc}%")).all()
    
    # Search for venues
    if name:
        venue_results = Venue.query.filter(Venue.name.ilike(f"%{name}%")).all()
    if loc:
        venue_results = Venue.query.filter(Venue.location.ilike(f"%{loc}%")).all()
    
    # Check which results are non-empty and return the appropriate response
    if show_results and not venue_results:
        result_type = "Show"
        results = [show.to_dict() for show in show_results]
    elif venue_results and not show_results:
        result_type = "Venue"
        results = [venue.to_dict() for venue in venue_results]
    else:
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
            db.session.add(new_show)
            db.session.commit()

            return jsonify({"message": "Show created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/show_shows', methods=['GET', 'POST'])
def show_shows():
    shows=Show.query.all()
    show_dicts = [show.to_dict() for show in shows]    
    return jsonify(show_dicts)

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

            db.session.commit()
            return jsonify({"message": "Show updated successfully"}), 200
        else:
            return jsonify({"error": "Show not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_shows/<int:show_id>', methods=['POST','GET'])
# @login_required
def delete_shows(show_id):
    try:
        this_show = Show.query.get(show_id)
        if this_show:
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
        db.session.add(new_venue)
        db.session.commit()

        return jsonify({"message": "Venue created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/show_venue', methods=['GET', 'POST'])
def show_venue():
    venues=Venue.query.all()
    venue_dict = [venue.to_dict() for venue in venues]
    return jsonify(venue_dict)
    
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
            
            db.session.commit()
            return jsonify({"message": "Venue updated successfully"}), 200
        else:
            return jsonify({"error": "Venue not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_venue/<int:venue_id>', methods=['POST','GET'])
# @login_required
def delete_venue(venue_id):
    try:
        this_venue = Venue.query.get(venue_id)
        if this_venue:
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
        print('inside')
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
            print('side')
            db.session.commit()
            return jsonify({'message': 'Tickets booked successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/csv_shows', methods=['GET', 'POST'])
def csv_shows():
    shows_data = Show.query.all()  # Assuming the model name is Show, not Venue
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
    print(shows_dicts)
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
    print(venues_dicts)
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=["id","name", "location", "capacity"])
    csv_writer.writeheader()
    csv_writer.writerows(venues_dicts)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=venues.csv"})

    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        this_user_id=current_user.id # type: ignore
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

@app.route('/bookings', methods=['GET'])
def bookings():
    try:
        # this_user_id = current_user.id
        tickets = Ticket.query.all()
        print(tickets)
        ticket_data = [ticket.to_dict() for ticket in (tickets)]
        return jsonify({'ticket_data': ticket_data})
    except Exception as e:
        return jsonify({'error': str(e)})




def render_show_table(shows):
    """Renders a list of shows as a HTML table."""
    table='<h2>Your monthly bookings</h2>'
    table += '<table border="1">'
    table += '<tr>'
    for field in ['name', 'datetime', 'rating', 'tag']:
        table += '<th>{}</th>'.format(field)
    table += '</tr>'
    for show in shows:
        table += '<tr>'
        for field in ['name', 'datetime', 'rating', 'tag']:
            table += '<td>{}</td>'.format(getattr(show, field))
        table += '</tr>'
    table += '</table>'
    return table

def send_email(to_email, subject, table):
    """Sends an email with the given HTML table as the body."""
    from_email = 'gautamgala5544@gmail.com' # Enter your email ID
    from_password = 'znjdsywcfkqxorrc' # Your password

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    part = MIMEText(table, 'html')
    msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(from_email, from_password)
    smtp.sendmail(from_email, to_email, msg.as_string())
    smtp.quit()

# @scheduler.task('cron', id='show_stats_monthly', year='*', month='*', day=1)
@celery.task
def show_stats_monthly():
    # Iterate over all users, get their shows, ratings, render in a html, send as email
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    start_date = datetime.datetime(year, month, 1)
    end_date = start_date.replace(month=start_date.month + 1, day=1) if start_date.month != 12 else start_date.replace(year=start_date.year + 1, month=1, day=1)
    users = User.query.filter_by().all()
    
    for user in users:
        id = user.id
        email = user.email
        tickets = db.session.query(Ticket).filter(
            Ticket.date_purchased >= start_date.isoformat(),
            Ticket.date_purchased < end_date.isoformat(),
            Ticket.user_id == id
        ).all()
        
        if tickets:  # Check  if the user has booked any tickets
            shows = []
            for ticket in tickets:
                show = Show.query.filter_by(id=ticket.show_id).first()
                shows.append(show)
            
            html = render_show_table(shows)
            month = datetime.datetime.now().month
            subject = "Entertainment Report for Month {} of {}".format(month, year)
            send_email(email, subject, html)

# @scheduler.task('cron', id='daily_reminders',hour=18, minute=0)
@celery.task
def daily_reminders():
    print('inside')
    today = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date()
    tomorrow = today + datetime.timedelta(days=1)
    users = User.query.all()
    for user in users:
        id = user.id
        email = user.email
        tickets = Ticket.query.filter(
            Ticket.user_id == id,
            Ticket.date_purchased >= today,
            Ticket.date_purchased < tomorrow
        ).all()
        

        if not tickets:
            html = "Hello {},<br>You haven't visited or booked anything today. We hope to see you soon!<br>Best regards,<br>nJOY Services Pvt. Ltd.".format(user.name)
            print((email,user))
            subject="Reminder: Visit or Book Something!"
            send_email(email,subject, html)

if __name__=='__main__':
    # users = User.query.all()
    # venues = Venue.query.all()
    # shows = Show.query.all()
    # print(f'Users: {users}\nVenues: {venues}\nShows: {shows}')
    db.create_all()
    # daily_reminders()  #uncomment to send daily emails and test the scheduler
    # show_stats_monthly()  #uncomment to send monthly emails and test the scheduler
    # daily_reminders.apply_async(eta=datetime.datetime.now().replace(hour=18, minute=0))
    # show_stats_monthly.apply_async()
    app.run(debug=True, port = 8000)

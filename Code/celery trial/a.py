from datetime import datetime
import datetime
from flask import Flask,  request, jsonify, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user,  login_user,   UserMixin
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from functools import wraps
import csv, io

app = Flask(__name__)



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
    from_email = 'gautamgala5544@gmail.com' # email ID
    from_password = 'znjdsywcfkqxorrc' # password

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
# @celery.task
def show_stats_monthly():
    # Iterating over all users, get their shows, ratings, render in a html, send as email
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
        
        if tickets:  
            shows = []
            for ticket in tickets:
                show = Show.query.filter_by(id=ticket.show_id).first()
                shows.append(show)
            
            html = render_show_table(shows)
            month = datetime.datetime.now().month
            subject = "Entertainment Report for Month {} of {}".format(month, year)
            send_email(email, subject, html)

# @scheduler.task('cron', id='daily_reminders',hour=18, minute=0)
# @celery.task
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
    db.create_all()
    # daily_reminders()  #uncomment to send daily emails and test the scheduler
    # show_stats_monthly()  #uncomment to send monthly emails and test the scheduler
    # daily_reminders.apply_async(eta=datetime.datetime.now().replace(hour=18, minute=0))
    # show_stats_monthly.apply_async()
    app.run(debug=True, port = 8000)

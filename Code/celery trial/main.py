# from worker import celery_app
# from flask import Flask, request

# app = Flask(__name__)
# cel = celery_app

# # from worker import celery_app

# @celery_app.task
# def add():
#     return "jai"

# @celery_app.task
# def sub(a,b):
#     return a-b

# @app.route('/task', methods=['GET', 'POST'])
# def task():
#     adda_result = add.delay()
#     res = f"Add Result: {adda_result.id}\nSubtract Result: "
    
#     return res

# if __name__ == '__main__':
#     app.run(debug=True)




from worker import celery_app
from flask import Flask, request
from celery.schedules import crontab

app = Flask(__name__)
cel = celery_app

@cel.task
def daily_task():
    # Your daily task code goes here
    return "This is the daily task result"

@app.route('/task', methods=['GET', 'POST'])
def task():
    adda_result = daily_task.apply_async()
    res = f"Daily Task Result (Task ID): {adda_result.id}"
    
    return res

if __name__ == '__main__':
    # Configure Celery Beat to schedule the daily_task
    cel.conf.beat_schedule = {
        'daily_task': {
            'task': 'main.daily_task',  # Specify the task name
            'schedule': crontab(hour=18, minute=0),  # Schedule it at 18:00
        },
    }
    
    app.run(debug=True)

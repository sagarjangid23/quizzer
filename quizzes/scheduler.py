from apscheduler.schedulers.background import BackgroundScheduler
from quizzes.task import update_status

scheduler = BackgroundScheduler()

def start_updation():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_status, id='update_status_job', trigger='cron', minute='*/5')
    scheduler.start()

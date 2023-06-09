from django.apps import AppConfig


class QuizzesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quizzes'
    
    def ready(self):
        from . import scheduler
        scheduler.start_updation()
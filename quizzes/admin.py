from django.contrib import admin
from .models import Choice, Question, Quiz, QuizAttempt, QuestionAttempt


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'answer']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score']

@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_quiz', 'question', 'get_answer', 'chosen_answer']
    
    def get_user(self, obj):
        return obj.quiz_attempt.user
    
    def get_quiz(self, obj):
        return obj.quiz_attempt.quiz
    
    def get_answer(self, obj):
        return obj.question.answer
    
    get_user.short_description = 'User'
    get_quiz.short_description = 'Quiz'
    get_answer.short_description = 'Answer'

from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.choice_text


class Question(models.Model):
    question_text = models.TextField()
    options = models.ManyToManyField(Choice, related_name='question_options')
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question_text


class Quiz(models.Model):
    
    class StatusEnum(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        FINISHED = 'FINISHED', _('Finished')
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=StatusEnum.choices, default=StatusEnum.INACTIVE.value)
    questions = models.ManyToManyField(Question, related_name='quiz_questions')
    
    class Meta:
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return self.title


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Quiz Attempts'
    
    def __str__(self):
        return f'{self.user} - {self.quiz.title}'


class QuestionAttempt(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="chosen_answers")
    
    class Meta:
        verbose_name_plural = 'Question Attempts'
    
    def __str__(self):
        return f'{self.quiz_attempt.user} - {self.question.question_text}'


@receiver(post_save, sender=QuestionAttempt)
def update_quiz_attempt_score(sender, instance, created, **kwargs):
    
    quiz_attempt = instance.quiz_attempt
    
    correct_answers = quiz_attempt.question_attempts.filter(
        chosen_answer__choice_text=F('question__answer__choice_text')
    ).count()
    
    total_questions = quiz_attempt.quiz.questions.count()
    
    score = (correct_answers / total_questions) * 100
    
    quiz_attempt.score = round(score, 2)
    quiz_attempt.save()
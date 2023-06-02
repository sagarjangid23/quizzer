from django.urls import path
from quizzes.views import QuizListView, QuizCreateView, ActiveQuizAPIView, QuizResultAPIView

urlpatterns = [
    path('', QuizCreateView.as_view(), name='all-quizzes'),
    path('/all', QuizListView.as_view(), name='quiz-create'),
    path('/active', ActiveQuizAPIView.as_view(), name='active-quiz'),
    path('/<uuid:id>/result', QuizResultAPIView.as_view(), name='quiz-result'),
]

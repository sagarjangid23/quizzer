from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import QuizSerializer, QuizListSerializer, QuizResultSerializer
from .models import Quiz, QuizAttempt
from rest_framework import status
from rest_framework.response import Response
import time
from datetime import timedelta


class QuizListView(APIView):
    
    @method_decorator(cache_page(120))
    def get(self, request):
        """
        API view to get a list of quizzes.
        """
        quizzes = Quiz.objects.all()
        
        serializer = QuizListSerializer(quizzes, many=True)
        
        quizzes_data = {
            'success': True,
            'quizzes': len(serializer.data),
            'data': serializer.data
        }
        
        return Response(quizzes_data, status=status.HTTP_200_OK)


class QuizCreateView(APIView):
    
    def post(self, request):
        """
        API view to create a quiz.
        """
        serializer = QuizSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'success': False, 'data': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)


class ActiveQuizAPIView(APIView):
    
    @method_decorator(cache_page(120))
    def get(self, request):
        """
        API view to get a list of active quizzes.
        """
        
        active_quizzes = Quiz.objects.filter(status=Quiz.StatusEnum.ACTIVE.value)
        
        serializer = QuizListSerializer(active_quizzes, many=True)
        
        active_quizzes_data = {
            'success': True,
            'active_quizzes': len(serializer.data),
            'data': serializer.data
        }
        
        return Response(active_quizzes_data, status=status.HTTP_200_OK)


class QuizResultAPIView(APIView):
    
    def get(self, request, id):
        """
        API view to get the result of a quiz.
        """
        try:
            quiz_attempt = QuizAttempt.objects.get(quiz__id=id)
        except QuizAttempt.DoesNotExist:
            return Response({'success': False, 'data': {"message": "Quiz result not found"}}, status=status.HTTP_404_NOT_FOUND)
        
        quiz = quiz_attempt.quiz
        
        if quiz.status == Quiz.StatusEnum.INACTIVE.value:
            return Response({'success': False, 'data': {"message": "Result not available for an Inactive quiz"}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        elif quiz.status == Quiz.StatusEnum.ACTIVE.value:
            return Response({'success': False, 'data': {"message": "Quiz not ended yet"}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        current_time = time.time()
        end_time = quiz.end_date.timestamp()
        five_minute_window = timedelta(minutes=5).total_seconds()
        
        if end_time <= current_time <= end_time + five_minute_window:
            # Display a message indicating the result is being prepared
            return Response({'success': True, 'data': {'message': "Please wait. We are preparing your result"}}, status=status.HTTP_202_ACCEPTED)
        
        serializer = QuizResultSerializer(quiz_attempt)
        
        result_message = 'Congratulations! You passed the quiz' if quiz_attempt.score >= 40 else 'Oops: You failed the quiz'
        result = {
            'success': True,
            'result_message': result_message,
            'result': serializer.data
        }
        return Response(result, status=status.HTTP_200_OK)

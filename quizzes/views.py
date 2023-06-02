from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import QuizSerializer, QuizListSerializer, QuizResultSerializer
from .models import Quiz, QuizAttempt
from rest_framework import status
from rest_framework.response import Response


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
    
    @method_decorator(cache_page(120))
    def get(self, request, id):
        """
        API view to get the result of a quiz.
        """
        try:
            quiz_attempt = QuizAttempt.objects.get(quiz__id=id)
            
            serializer = QuizResultSerializer(quiz_attempt)
            
            result = {
                'success': True,
                'result_message': 'Congratulations! You passed the quiz' if quiz_attempt.score >= 40 else 'Oops: You failed the quiz',
                'result': serializer.data
            }
            
            return Response(result, status=status.HTTP_200_OK)
        except QuizAttempt.DoesNotExist:
            return Response({'success': False, 'data': {"message": "Quiz result not found"}}, status=status.HTTP_404_NOT_FOUND)

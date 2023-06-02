from rest_framework import serializers
from quizzes.models import Choice, Question, Quiz, QuizAttempt
from django.db import transaction
from django.utils import timezone


class QuizListSerializer(serializers.ModelSerializer):
    
    total_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id','title', 'status', 'start_date', 'end_date', 'total_questions']
        
    def get_total_questions(self, obj):
        return len(obj.questions.all())


class QuestionSerializer(serializers.Serializer):
    
    question_text = serializers.CharField()
    options = serializers.DictField(child=serializers.CharField(max_length=255))
    answer = serializers.IntegerField()
    
    def to_representation(self, value):
        return {
            "question": value.question_text,
            "options": [option.choice_text for option in value.options.all()],
            "answer": value.answer.choice_text
        }
    
    def validate_options(self, options):
        
        if len(options) != 4:
            raise serializers.ValidationError("Exactly 4 options are required")
        
        if len(set(options.values())) != len(options.values()):
            raise serializers.ValidationError("Duplicate option found")
        
        if not set(options.keys()).issubset({'1', '2', '3', '4'}):
            raise serializers.ValidationError("Invalid option keys. Options must be labeled between 1 and 4.")
        
        return options
    
    def validate_answer(self, answer):
        
        if not answer in [1,2,3,4]:
            raise serializers.ValidationError("Invalid answer. Only options 1 to 4 are allowed.")
        
        return answer


class QuizSerializer(serializers.ModelSerializer):
    
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'start_date', 'end_date', 'questions']
        
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "start_date": value.start_date,
            "end_date": value.end_date,
            "total_questions": len(value.questions.all()),
            "questions": [
                {
                    "question": question.question_text,
                    "options": {num: option.choice_text for num, option in enumerate(question.options.all(), start=1)}
                }
                for question in value.questions.all()
            ],
        }
    
    def validate_questions(self, questions):
        
        questions_text = [question['question_text'] for question in questions]
        
        if len(set(questions_text)) != len(questions_text):
            raise serializers.ValidationError("Duplicate questions found")
        
        if len(questions_text) < 5:
            raise serializers.ValidationError("At least 5 questions are required")
        
        return questions
    
    def validate(self, attrs):
        
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and start_date < timezone.now():
            raise serializers.ValidationError({"start_date": "Start date must be in the future or current"})
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"start_date": "End date must be after start date"})
        
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        
        title_data = validated_data.pop('title')
        start_date_data = validated_data.pop('start_date')
        end_date_data = validated_data.pop('end_date')
        questions_data = validated_data.pop('questions')
        
        quiz = Quiz.objects.create(
            title=title_data,
            start_date=start_date_data,
            end_date=end_date_data
        )
        
        for question_data in questions_data:
            question_text = question_data['question_text']
            options_data = question_data['options']
            options_values = question_data['options'].values()
            answer_data = options_data[str(question_data['answer'])]
            
            option_objs = [Choice.objects.get_or_create(choice_text=option_value)[0] for option_value in options_values]
            answer, _ = Choice.objects.get_or_create(choice_text=answer_data)
            
            question, created = Question.objects.get_or_create(question_text=question_text, answer=answer)
            
            if not created and question.options.filter(choice_text__in=option_objs).exists():
                pass
            else:
                question.answer = answer
                question.options.set(option_objs)
                quiz.questions.add(question)
            quiz.questions.add(question)
        
        return quiz


class QuizResultSerializer(serializers.ModelSerializer):
    
    user_name = serializers.SerializerMethodField()
    quiz_name = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    question_answers = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizAttempt
        fields = ['user_name','quiz_name', 'percentage', 'question_answers']
    
    def get_user_name(self, obj):
        return str(obj.user.username)
    
    def get_quiz_name(self, obj):
        return str(obj.quiz.title)

    def get_percentage(self, obj):
        return f"{obj.score}%"
    
    def get_question_answers(self, obj):
        
        question_answers_list = [
            {
                "Question Text": str(question_attempt.question),
                "Chosen Answer": str(question_attempt.chosen_answer),
                "Correct Answer": str(question_attempt.question.answer),
            }
            for question_attempt in obj.question_attempts.all()
        ]
        
        return question_answers_list

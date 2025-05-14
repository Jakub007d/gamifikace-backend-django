"""
Serializéry pre Django REST Framework pre aplikáciu Gamifikace.

Obsahuje serializéry pre entity ako sú Question, User, Course, Score, Comment, Answer, Okruh, ChalangeQuestion a Achievement.
"""

from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Question.

    Serializuje polia otázky na použitie v API.
    """
    class Meta:
        model = Question
        fields = ['id', 'name', 'text', 'approved', 'visible', 'created_by', 'likes', 'created_at', 'okruh', 'is_text_question', 'ai_context', 'reported']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializér pre používateľa.

    Serializuje základné údaje používateľa.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'is_staff')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializér pre registráciu používateľa s validáciou hesiel a registračného kódu.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')
    registration_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'registration_code', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """
        Overí zhodu hesiel a správnosť registračného kódu.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Heslá sa sa nezhodujú."})
        if attrs['registration_code'] != 'ObhajobaSecretCode':
            raise serializers.ValidationError({"registration_code": "Nesprávny registračný kód."})
        return attrs

    def create(self, validated_data):
        """
        Vytvorí nového používateľa po registrácii.
        """
        validated_data.pop('password2')
        validated_data.pop('registration_code')
        user = User.objects.create_user(**validated_data)
        return user


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Course.

    Obsahuje základné údaje o kurze.
    """
    class Meta:
        model = Course
        fields = ('id', 'name', 'full_name')


class ScoreSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Score.

    Obsahuje aj username používateľa a názov kurzu.
    """
    username = serializers.CharField(source='user.username')
    coursename = serializers.CharField(source='course.name')

    class Meta:
        model = Score
        fields = ('id', 'course', 'user', 'coursename', 'username', 'points')


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Comment.

    Obsahuje aj username autora komentára.
    """
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'created_by', 'likes', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Answer.

    Serializuje odpovede k otázkam.
    """
    class Meta:
        model = Answer
        fields = ['id', 'answer_type', 'text', 'question']


class OkruhSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Okruh.

    Obsahuje aj informácie o dokončení okruhu.
    """
    class Meta:
        model = Okruh
        fields = ('id', 'name', 'description', 'available', 'course', 'finished_by')


class ChallangeQuestionSerializer(serializers.ModelSerializer):
    """
    Serializér pre model ChalangeQuestion.

    Serializuje iba priradenú otázku.
    """
    class Meta:
        model = ChalangeQuestion
        fields = ['question']


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializér pre model Achievement.

    Obsahuje informácie o udelených achievementoch.
    """
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'awarded_to')


class CourseCompletionSerializer(serializers.Serializer):
    """
    Serializér pre percentuálne dokončenie kurzu.

    Attributes:
        course (str): Názov kurzu.
        completion_percentage (float): Percento dokončenia kurzu.
    """
    course = serializers.CharField()
    completion_percentage = serializers.FloatField()

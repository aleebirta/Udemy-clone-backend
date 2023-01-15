from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from userextend.serializers import UserSerializer
from courses.models import Course, Comment, CourseSection, Episode
from rest_framework import serializers, status


class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_student')
    author = UserSerializer()
    image_url = serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model= Course
        fields = [
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
        ]

class EpisodeUnpaidSerializer(ModelSerializer):
    length = serializers.CharField(source='video_length_time')

    class Meta:
        model = Episode
        exclude = [
            'title',
            'length',
            'id',

        ]

class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = [
            'id'
        ]


class CourseSectionUnpaidSerializer(ModelSerializer):
    episodes = EpisodeUnpaidSerializer(many=True)
    total_duration = serializers.CharField(source='total_length')

    class Meta:
        model = CourseSection
        fields = [
            'section_title',
            'section_number',
            'episodes',
            'total_duration',
        ]



class EpisodePaidSerializer(ModelSerializer):
    length = serializers.CharField(source='video_length_time')

    class Meta:
        model = Episode
        exclude = [
            'file',
            'length',
            'title',

        ]

class CourseUnpaidSerilizer(ModelSerializer):
    comments = CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionUnpaidSerializer(many=True)
    student_no = serializers.IntegerField(source='enrolled_student')
    total_lectures = serializers.IntegerField(source='total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        exclude = [
            'id'

        ]

class CoursePaidSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionUnpaidSerializer(many=True)
    student_no = serializers.IntegerField(source='enrolled_student')
    total_lectures = serializers.IntegerField(source='total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        exclude = [
            'id'

        ]

class CourseSectionPaidSerializer(ModelSerializer):
    episode = EpisodePaidSerializer(many=True)
    total_duration = serializers.CharField(source='total_length')

    class Meta:
        model = CourseSection
        fields = [
            'section_title',
            'episode',
            'total_duration',
        ]



class CourseListSerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='enrolled_student')
    author = UserSerializer()
    description = serializers.CharField(source='description')
    total_lectures = serializers.IntegerField(source='total_lectures')

    class Meta:
        model = Course
        fields = [
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
            'description',
            'total_lectures'
        ]


class CartItemSerializer(ModelSerializer):
    author = UserSerializer()
    image_url = serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        field = [
            'author',
            'title',
            'price',
            'image_url'
        ]

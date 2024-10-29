from rest_framework import serializers
from .models import MyCart , MyCourse

class MyCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCart
        fields = ['id', 'user', 'course_name']

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = ['id', 'user', 'course_name', 'bought_on']

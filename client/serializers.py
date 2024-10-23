from rest_framework import serializers
from .models import MyCart , MyCourse

class MyCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCart
        fields = ['id', 'user', 'courses']

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = ['id', 'user', 'courses', 'bought_on', 'status']

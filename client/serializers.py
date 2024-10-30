from rest_framework import serializers
from .models import MyCart , MyCourse
from base.models import CustomUser

class MyCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCart
        fields = ['id','course_name']

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = ['id','course_name', 'bought_on']

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'profile_picture','username', 'first_name', 'last_name', 'email', 'bio', 'role', 'joined_at']
        

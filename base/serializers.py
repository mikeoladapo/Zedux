from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Instructor, Course, Category, CourseMaterial

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'profile_picture', 'first_name', 'last_name', 'email', 'bio', 'role', 'joined_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.profile_picture = validated_data.get('profile_picture',instance.profile_picture)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)
        instance.bio = validated_data.get('bio',instance.bio)
        instance.role = validated_data.get('role',instance.role)
        instance.password = validated_data.get('password',instance.password)
        return instance
    
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['instructor_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['text_file', 'video_file']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'category_name', 'duration', 'instructor_name', 'amount', 'course_materials']


from rest_framework import serializers
from .models import CustomUser, Instructor, Course, Category, CourseMaterial

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role', 'profile_picture', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.profile_picture = validated_data.get('profile_picture',instance.profile_picture)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)
        instance.bio = validated_data.get('bio',instance.bio)
        instance.role = validated_data.get('role',instance.role)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id','instructor_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CourseMaterialSerializer(serializers.ModelSerializer):
    video_file = serializers.URLField(source='video_file.url', read_only=True)
    certificate = serializers.URLField(source='certificate.url', read_only=True)
    other_file = serializers.URLField(source='other_file.url', read_only=True)
    class Meta:
        model = CourseMaterial
        fields = ['id','course_name', 'instructor', 'video_file', 'certificate', 'other_file', 'text_file']



class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'category_name', 'duration', 'amount', 'course_material','instructor']
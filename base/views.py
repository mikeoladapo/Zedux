from django.shortcuts import render
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from .serializers import CustomUserSerializer ,InstructorSerializer,CategorySerializer,CourseSerializer,CourseMaterialSerializer
from rest_framework import viewsets

class CustomUserViewset(viewsets.ViewSet):
    def list ()
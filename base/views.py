from rest_framework.response import Response 
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from .serializers import CustomUserSerializer ,InstructorSerializer,CategorySerializer,CourseSerializer,CourseMaterialSerializer
from rest_framework import viewsets

class CustomUserViewset(viewsets.ViewSet):
    def list(self,request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CustomUserSerializer(user,many=False)
        return Response(serializer.data)
    
class InstructorViewset(viewsets.ViewSet):
    def list(self,request):
        queryset = Instructor.objects.all()
        serializer = InstructorSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = Instructor.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = InstructorSerializer(user,many=False)
        return Response(serializer.data)
        

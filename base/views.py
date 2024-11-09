from rest_framework.response import Response 
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from .serializers import CustomUserSerializer ,InstructorSerializer,CategorySerializer,CourseSerializer,CourseMaterialSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsInstructor,IsCourseOwner

class CustomUserViewset(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self,request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CustomUserSerializer(user,many=False)
        return Response(serializer.data)

    def create(self,request):
        serializer = CustomUserSerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CustomUserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InstructorViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAdminUser]
        elif self.action == "update":
            permission_classes = [IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self,request):
        queryset = Instructor.objects.all()
        serializer = InstructorSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = Instructor.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = InstructorSerializer(user,many=False)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = InstructorSerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        queryset = Instructor.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = InstructorSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = Instructor.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action=="create":
            permission_classes = [IsAdminUser]
        elif self.action == "update":
            permission_classes = [IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CategorySerializer(user,many=False)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = CategorySerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CategorySerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset,pk=pk)   
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class CourseViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action=="create":
            permission_classes = [IsAuthenticated,IsAdminUser|IsInstructor]
        elif self.action == "update":
            permission_classes = [IsAuthenticated,IsCourseOwner]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated,IsAdminUser|IsCourseOwner]
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self,request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CourseSerializer(user,many=False)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = CourseSerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CourseSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseMaterialViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action=="create":
            permission_classes = [IsAuthenticated,IsAdminUser|IsCourseOwner]
        elif self.action == "update":
            permission_classes = [IsAuthenticated,IsAdminUser|IsCourseOwner]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated,IsAdminUser|IsCourseOwner]
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self,request):
        queryset = CourseMaterial.objects.all()
        serializer =CourseMaterialSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = CourseMaterial.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CourseMaterialSerializer(user,many=False)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = CourseMaterialSerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        queryset = CourseMaterial.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CourseMaterialSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = CourseMaterial.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
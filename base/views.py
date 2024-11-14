from rest_framework.response import Response 
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from .serializers import CustomUserSerializer ,InstructorSerializer,CategorySerializer,CourseSerializer,CourseMaterialSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsInstructor,IsCourseOwner
import cloudinary.uploader

class CustomUserViewset(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def _handle_file_upload(self,request,custom_user=None):
        if "profile_picture" in request.FILES :
            profile_picture_upload = cloudinary.uploader.upload(
                request.FILES["profile_picture"],resource_type="image"
            )
            profile_picture_url = profile_picture_upload.get('url')
            custom_user.profile_picture = profile_picture_url
        custom_user.first_name = request.data.get('first_name',custom_user.first_name)
        custom_user.last_name = request.data.get('last_name',custom_user.last_name)
        custom_user.username = request.data.get('username',custom_user.username)
        custom_user.email = request.data.get('email',custom_user.email)
        custom_user.bio = request.data.get('bio',custom_user.bio)
        custom_user.role = request.data.get('role',custom_user.role)
        custom_user.is_active = request.data.get('is_active',custom_user.is_active)
        custom_user.is_staff = request.data.get('is_staff',custom_user.is_staff)
        return custom_user   
    
    def list(self,request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CustomUserSerializer(user,many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data,many=False)
        if serializer.is_valid():
            custom_user = serializer.save(commit=False)
            custom_user = self._handle_file_upload(request,custom_user)
            custom_user.save()
            saved_serializer = CustomUserSerializer(custom_user)
            return Response(saved_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        try:
            custom_user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(custom_user,data=request.data,partial=True)
        if serializer.is_valid():
            custom_user = self._handle_file_upload(request,custom_user)
            custom_user.save()
            saved_serializer = CustomUserSerializer(custom_user)
            return Response(saved_serializer.data , status=status.HTTP_200_OK)
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
    
    def _handle_file_upload(self,request,course_material=None):
        if "video_file" in request.FILES:
            video_file_upload = cloudinary.uploader.upload(
                request.FILES["video_file"],resource_type ="video"
            )
            video_file_url = video_file_upload.get("url")
            course_material.video_file = video_file_url
        if "other_file" in request.FILES:
            other_file_upload = cloudinary.uploader.upload(
                request.FILES["other_file"],resource_type ="auto"
            )
            other_file_url = other_file_upload.get("url")
            course_material.other_file = other_file_url
        if "certificate" in request.FILES:
            certificate_upload = cloudinary.uploader.upload(
                request.FILES["certificate"],resource_type ="auto"
            )
            certificate_url = certificate_upload.get("url")
            course_material.certificate = certificate_url

        course_material.course_name = request.data.get("course_name",course_material.course_name)
        course_material.instructor = request.data.get("instructor",course_material.instructor)
        course_material.text_file = request.data.get("text_file",course_material.text_file)


    def list(self,request):
        queryset = CourseMaterial.objects.all()
        serializer =CourseMaterialSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = CourseMaterial.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = CourseMaterialSerializer(user,many=False)
        return Response(serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer = CourseMaterialSerializer(data=request.data,many=False)
        if serializer.is_valid():
            course_material = serializer.save(commit=False)
            course_material = self._handle_file_upload(request,course_material)
            course_material.save()
            saved_serializer = CourseMaterialSerializer(course_material)
            return Response(saved_serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        try:
            course_material = CourseMaterial.objects.get(pk=pk)
        except CourseMaterial.DoesNotExist:
            return Response({"error": "Course material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseMaterialSerializer(course_material,data=request.data)
        if serializer.is_valid():
            course_material = serializer.save(commit)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        queryset = CourseMaterial.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
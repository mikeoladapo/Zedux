from rest_framework.response import Response 
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from .serializers import CustomUserSerializer ,InstructorSerializer,CategorySerializer,CourseSerializer,CourseMaterialSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .permissions import IsInstructor,IsCourseOwner
import cloudinary.uploader
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

class LoginViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(
                description="Login successful, returns JWT tokens",
                response={
                    "type": "object",
                    "properties": {
                        "refresh": {"type": "string"},
                        "access": {"type": "string"},
                        "message": {"type": "string"},
                        "api_base_url": {"type": "string"},
                    }
                }
            ),
            400: OpenApiResponse(description="Bad Request: Missing username or password"),
            401: OpenApiResponse(description="Unauthorized: Invalid username or password")
        }
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Please provide both username and password."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful. Use the API base URL to start interacting with the API.",
                    "api_base_url": "http://127.0.0.1:8000/api/"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description="Logout successful"),
            400: OpenApiResponse(description="Bad Request: Missing refresh token"),
            401: OpenApiResponse(description="Unauthorized: Invalid or expired refresh token")
        }
    )
    @action(detail=False, methods=["post"])
    def logout(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required for logout."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )
class CustomUserViewset(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def _handle_file_upload(self, request, custom_user=None):
        if "profile_picture" in request.FILES:
            profile_picture_upload = cloudinary.uploader.upload(
                request.FILES["profile_picture"], resource_type="image"
            )
            profile_picture_url = profile_picture_upload.get('url')
            custom_user.profile_picture = profile_picture_url
        custom_user.first_name = request.data.get('first_name', custom_user.first_name)
        custom_user.last_name = request.data.get('last_name', custom_user.last_name)
        custom_user.username = request.data.get('username', custom_user.username)
        custom_user.email = request.data.get('email', custom_user.email)
        custom_user.bio = request.data.get('bio', custom_user.bio)
        custom_user.role = request.data.get('role', custom_user.role)
        custom_user.is_active = request.data.get('is_active', custom_user.is_active)
        custom_user.is_staff = request.data.get('is_staff', custom_user.is_staff)
        return custom_user

    @extend_schema(
        responses=OpenApiResponse(
            description="List of users",
            response=CustomUserSerializer(many=True)  # Proper response schema for the list of users
        )
    )
    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiResponse(
            description="Retrieve user by ID",
            response=CustomUserSerializer  # Correct response schema for a single user
        ),
        parameters=[OpenApiParameter("pk", description="User ID", required=True, type=int)]
    )
    def retrieve(self, request, pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)

    @extend_schema(
        request=CustomUserSerializer,  # Request body schema
        responses={
            201: OpenApiResponse(
                description="User created successfully",
                response=CustomUserSerializer  # Correct response schema for successful user creation
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data")  # 400 Bad Request response
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data, many=False)
        if serializer.is_valid():
            custom_user = serializer.save(commit=False)
            custom_user = self._handle_file_upload(request, custom_user)
            custom_user.save()
            saved_serializer = CustomUserSerializer(custom_user)
            return Response(saved_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CustomUserSerializer,  # Request body schema
        responses={
            200: OpenApiResponse(
                description="User updated successfully",
                response=CustomUserSerializer  # Correct response schema for successful update
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data"),  # 400 Bad Request response
            404: OpenApiResponse(description="User not found")  # 404 User not found response
        },
        parameters=[OpenApiParameter("pk", description="User ID", required=True, type=int)]
    )
    def update(self, request, pk):
        try:
            custom_user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(custom_user, data=request.data)
        if serializer.is_valid():
            custom_user = serializer.save(commit=False)
            custom_user = self._handle_file_upload(request, custom_user)
            custom_user.save()
            saved_serializer = CustomUserSerializer(custom_user)
            return Response(saved_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="User deleted successfully"),  # 204 No content for successful delete
            404: OpenApiResponse(description="User not found")  # 404 User not found response
        },
        parameters=[OpenApiParameter("pk", description="User ID", required=True, type=int)]
    )
    def destroy(self, request, pk):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
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

    @extend_schema(
        responses=OpenApiResponse(
            description="List of instructors",
            response=InstructorSerializer(many=True)  # Correct schema for a list of instructors
        )
    )
    def list(self, request):
        queryset = Instructor.objects.all()
        serializer = InstructorSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiResponse(
            description="Retrieve instructor by ID",
            response=InstructorSerializer  # Correct schema for retrieving a single instructor
        ),
        parameters=[OpenApiParameter("pk", description="Instructor ID", required=True, type=int)]
    )
    def retrieve(self, request, pk):
        queryset = Instructor.objects.all()
        instructor = get_object_or_404(queryset, pk=pk)
        serializer = InstructorSerializer(instructor, many=False)
        return Response(serializer.data)

    @extend_schema(
        request=InstructorSerializer,  # Request body schema for creating an instructor
        responses={
            201: OpenApiResponse(
                description="Instructor created successfully",
                response=InstructorSerializer  # Correct response schema for instructor creation
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data")  # 400 Bad Request for invalid data
        }
    )
    def create(self, request):
        serializer = InstructorSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=InstructorSerializer,  # Request body schema for updating an instructor
        responses={
            200: OpenApiResponse(
                description="Instructor updated successfully",
                response=InstructorSerializer  # Correct response schema for successful update
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data"),  # 400 for invalid data
            404: OpenApiResponse(description="Instructor not found")  # 404 if instructor not found
        },
        parameters=[OpenApiParameter("pk", description="Instructor ID", required=True, type=int)]  # Include pk for parameter
    )
    def update(self, request, pk):
        queryset = Instructor.objects.all()
        instructor = get_object_or_404(queryset, pk=pk)
        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Instructor deleted successfully"),  # 204 for successful deletion
            404: OpenApiResponse(description="Instructor not found")  # 404 if instructor not found
        },
        parameters=[OpenApiParameter("pk", description="Instructor ID", required=True, type=int)]  # Include pk for parameter
    )
    def destroy(self, request, pk):
        queryset = Instructor.objects.all()
        instructor = get_object_or_404(queryset, pk=pk)
        instructor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="User successfully became an instructor",
                response=InstructorSerializer  # Correct response schema for becoming an instructor
            ),
            400: OpenApiResponse(description="Bad Request: User is already an instructor")  # 400 if user is already an instructor
        }
    )
    @action(detail=False, methods=['post'])
    def become_an_instructor(self, request):
        if Instructor.objects.filter(instructor=request.user).exists():
            return Response(
                {"error": "User is already an instructor"},
                status=status.HTTP_400_BAD_REQUEST
            )
        new_instructor = Instructor.objects.create(instructor=request.user,
                                                   bio=getattr(request.user, 'bio', ''))  # Use empty string if bio is missing
        serializer = InstructorSerializer(new_instructor)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CategoryViewset(viewsets.ViewSet):
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

    @extend_schema(
        responses=OpenApiResponse(
            description="List of categories",
            response=CategorySerializer(many=True)  # Correct response schema for a list of categories
        )
    )
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiResponse(
            description="Retrieve category by ID",
            response=CategorySerializer  # Correct response schema for retrieving a single category
        ),
        parameters=[OpenApiParameter("pk", description="Category ID", required=True, type=int)]  # Include pk for parameter
    )
    def retrieve(self, request, pk):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)

    @extend_schema(
        request=CategorySerializer,  # Request body schema for creating a category
        responses={
            201: OpenApiResponse(
                description="Category created successfully",
                response=CategorySerializer  # Correct response schema for successful creation
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data")  # 400 for invalid data
        }
    )
    def create(self, request):
        serializer = CategorySerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CategorySerializer,  # Request body schema for updating a category
        responses={
            200: OpenApiResponse(
                description="Category updated successfully",
                response=CategorySerializer  # Correct response schema for successful update
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data"),  # 400 for invalid data
            404: OpenApiResponse(description="Category not found")  # 404 if category not found
        },
        parameters=[OpenApiParameter("pk", description="Category ID", required=True, type=int)]  # Include pk for parameter
    )
    def update(self, request, pk):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Category deleted successfully"),  # 204 for successful deletion
            404: OpenApiResponse(description="Category not found")  # 404 if category not found
        },
        parameters=[OpenApiParameter("pk", description="Category ID", required=True, type=int)]  # Include pk for parameter
    )
    def destroy(self, request, pk):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CourseViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminUser | IsInstructor]
        elif self.action == "update":
            permission_classes = [IsAuthenticated, IsCourseOwner]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAdminUser | IsCourseOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        responses=OpenApiResponse(
            description="List of courses",
            response=CourseSerializer(many=True)  # Correct schema for listing multiple courses
        )
    )
    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiResponse(
            description="Retrieve course by ID",
            response=CourseSerializer  # Correct schema for a single course retrieval
        ),
        parameters=[OpenApiParameter("pk", description="Course ID", required=True, type=int)]  # pk parameter
    )
    def retrieve(self, request, pk):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)

    @extend_schema(
        request=CourseSerializer,  # Request schema for course creation
        responses={
            201: OpenApiResponse(
                description="Course created successfully",
                response=CourseSerializer  # Correct schema for successful creation
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data")  # 400 for invalid data
        }
    )
    def create(self, request):
        serializer = CourseSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CourseSerializer,  # Request schema for course update
        responses={
            200: OpenApiResponse(
                description="Course updated successfully",
                response=CourseSerializer  # Correct schema for successful update
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data"),  # 400 for invalid data
            404: OpenApiResponse(description="Course not found")  # 404 if course not found
        },
        parameters=[OpenApiParameter("pk", description="Course ID", required=True, type=int)]  # pk parameter
    )
    def update(self, request, pk):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Course deleted successfully"),  # 204 for successful deletion
            404: OpenApiResponse(description="Course not found")  # 404 if course not found
        },
        parameters=[OpenApiParameter("pk", description="Course ID", required=True, type=int)]  # pk parameter
    )
    def destroy(self, request, pk):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CourseMaterialViewset(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminUser | IsCourseOwner]
        elif self.action == "update":
            permission_classes = [IsAuthenticated, IsAdminUser | IsCourseOwner]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAdminUser | IsCourseOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def _handle_file_upload(self, request, course_material=None):
        # Handle file uploads for video, other files, and certificates
        if "video_file" in request.FILES:
            video_file_upload = cloudinary.uploader.upload(
                request.FILES["video_file"], resource_type="video"
            )
            course_material.video_file = video_file_upload.get("url")
        if "other_file" in request.FILES:
            other_file_upload = cloudinary.uploader.upload(
                request.FILES["other_file"], resource_type="auto"
            )
            course_material.other_file = other_file_upload.get("url")
        if "certificate" in request.FILES:
            certificate_upload = cloudinary.uploader.upload(
                request.FILES["certificate"], resource_type="auto"
            )
            course_material.certificate = certificate_upload.get("url")

        # Set other fields from request data
        course_material.course_name = request.data.get("course_name", course_material.course_name)
        course_material.instructor = request.data.get("instructor", course_material.instructor)
        course_material.text_file = request.data.get("text_file", course_material.text_file)
        return course_material

    @extend_schema(
        responses=OpenApiResponse(
            description="List of course materials",
            response=CourseMaterialSerializer(many=True)  # Correct schema for listing course materials
        )
    )
    def list(self, request):
        queryset = CourseMaterial.objects.all()
        serializer = CourseMaterialSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiResponse(
            description="Retrieve course material by ID",
            response=CourseMaterialSerializer  # Correct schema for retrieving a single course material
        ),
        parameters=[OpenApiParameter("pk", description="Course Material ID", required=True, type=int)]
    )
    def retrieve(self, request, pk):
        course_material = get_object_or_404(CourseMaterial, pk=pk)
        serializer = CourseMaterialSerializer(course_material)
        return Response(serializer.data)

    @extend_schema(
        request=CourseMaterialSerializer,  # Define request body schema for creating course material
        responses={
            201: OpenApiResponse(
                description="Course material created successfully",
                response=CourseMaterialSerializer  # Correct response schema for successful creation
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data")  # Error response for invalid data
        }
    )
    def create(self, request):
        serializer = CourseMaterialSerializer(data=request.data)
        if serializer.is_valid():
            course_material = serializer.save(commit=False)
            course_material = self._handle_file_upload(request, course_material)
            course_material.save()
            saved_serializer = CourseMaterialSerializer(course_material)
            return Response(saved_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CourseMaterialSerializer,  # Define request body schema for updating course material
        responses={
            200: OpenApiResponse(
                description="Course material updated successfully",
                response=CourseMaterialSerializer  # Correct response schema for successful update
            ),
            400: OpenApiResponse(description="Bad Request: Invalid data"),
            404: OpenApiResponse(description="Course material not found")
        },
        parameters=[OpenApiParameter("pk", description="Course Material ID", required=True, type=int)]
    )
    def update(self, request, pk):
        try:
            course_material = CourseMaterial.objects.get(pk=pk)
        except CourseMaterial.DoesNotExist:
            return Response({"error": "Course material not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseMaterialSerializer(course_material, data=request.data)
        if serializer.is_valid():
            course_material = serializer.save(commit=False)
            course_material = self._handle_file_upload(request, course_material)
            saved_serializer = CourseMaterialSerializer(course_material)
            return Response(saved_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Course material deleted successfully"),
            404: OpenApiResponse(description="Course material not found")
        },
        parameters=[OpenApiParameter("pk", description="Course Material ID", required=True, type=int)]
    )
    def destroy(self, request, pk):
        course_material = get_object_or_404(CourseMaterial, pk=pk)
        course_material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
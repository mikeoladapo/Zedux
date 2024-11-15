from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from base.models import Course
from .models import MyCart,MyCourse
from .serializers import MyCartSerializer,MyCourseSerializer,MyProfileSerializer
from django.utils import timezone 
from base.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsMyOwner,IsMyCart
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

class MyCartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsMyCart]

    @extend_schema(
        responses={200: MyCartSerializer(many=True)},
        description="List all items in the user's cart"
    )
    def list(self, request):
        queryset = MyCart.objects.filter(user=request.user)
        serializer = MyCartSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(
        responses={200: MyCartSerializer(many=False)},
        parameters=[OpenApiTypes.INT],
        description="Retrieve a specific cart item by ID"
    )
    def retrieve(self, request, pk):
        try:
            queryset = MyCart.objects.get(pk=pk, user=request.user)
            serializer = MyCartSerializer(queryset, many=False)
            return Response(serializer.data)
        except MyCart.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={200: OpenApiResponse(description="Successfully deleted the cart item")},
        description="Delete a specific cart item by ID"
    )
    def destroy(self, request, pk):
        try:
            queryset = MyCart.objects.get(pk=pk, user=request.user)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except MyCart.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={201: MyCartSerializer},
        parameters=[OpenApiTypes.INT],
        description="Add a course to the user's cart"
    )
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course Not found'}, status=status.HTTP_404_NOT_FOUND)
        if MyCart.objects.filter(user=request.user, course=course_id).exists():
            return Response({'error': 'Course already exists in Cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item = MyCart.objects.create(user=request.user, course=course)
        serializer = MyCartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyCourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsMyOwner]

    @extend_schema(
        responses={200: MyCourseSerializer(many=True)},
        description="List all courses owned by the user"
    )
    def list(self, request):
        queryset = MyCourse.objects.filter(user=request.user)
        serializer = MyCourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={200: MyCourseSerializer(many=False)},
        parameters=[OpenApiTypes.INT],
        description="Retrieve a specific course by ID"
    )
    def retrieve(self, request, pk):
        try:
            queryset = MyCourse.objects.get(pk=pk, user=request.user)
            serializer = MyCourseSerializer(queryset, many=False)
            return Response(serializer.data)
        except MyCourse.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={200: OpenApiResponse(description="Successfully deleted the course item")},
        description="Delete a specific course item by ID"
    )
    def destroy(self, request, pk):
        try:
            queryset = MyCourse.objects.get(pk=pk, user=request.user)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except MyCourse.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={201: MyCourseSerializer},
        parameters=[OpenApiTypes.INT],
        description="Add a course to the user's list of courses"
    )
    @action(detail=False, methods=['post'])
    def add_to_my_course(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course Not found'}, status=status.HTTP_404_NOT_FOUND)
        if MyCourse.objects.filter(user=request.user, course=course).exists():
            return Response({'error': 'Course already exists in your list of courses'}, status=status.HTTP_400_BAD_REQUEST)
        new_course = MyCourse.objects.create(user=request.user, course=course, bought_on=timezone.now())
        serializer = MyCourseSerializer(new_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

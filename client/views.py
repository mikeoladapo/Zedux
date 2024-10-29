from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from base.models import Course
from .models import MyCart,MyCourse
from .serializers import MyCartSerializer,MyCourseSerializer
from django.utils import timezone
class MyCartViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = MyCart.objects.filter(user=request.user)
        serializer = MyCartSerializer(queryset)
        return Response(serializer.data)
    def retrieve(self,request,pk):
        try:
            queryset = MyCart.objects.get(pk=pk,user=request.user)
            serializer = MyCartSerializer(queryset,many=False)
            return Response(serializer.data)
        except MyCart.DoesNotExist:
            return Response({'error': 'Not found'},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk):
        try:
            queryset = MyCart.objects.get(pk=pk,user=request.user)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except MyCart.DoesNotExist:
            return Response({'error': 'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False,methods=['post'])  
    def add_to_cart(self,request,course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error':'Course Not found'},status=status.HTTP_404_NOT_FOUND)
        if MyCart.objects.filter(user=request.user,course=course_id).exists():
            return Response({'error':'Course already exists in Cart'},status=status.HTTP_400_BAD_REQUEST)
        cart_item = MyCart.objects.create(user=request.user,course=course)
        serializer = MyCartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MyCourseViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = MyCourse.objects.filter(user=request.user)
        serializer = MyCourseSerializer(queryset)
        return Response(serializer.data)
    def retrieve(self,request,pk):
        try:
            queryset = MyCourse.objects.get(pk=pk,user=request.user)
            serializer = MyCourseSerializer(queryset,many=False)
            return Response(serializer.data)
        except MyCourse.DoesNotExist:
            return Response({'error': 'Not found'},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk):
        try:
            queryset = MyCourse.objects.get(pk=pk,user=request.user)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except MyCourse.DoesNotExist:
            return Response({'error': 'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False,methods=['post']) 
    def add_to_mycourse(self,request,course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error':'Course Not found'},status=status.HTTP_404_NOT_FOUND)
        if MyCourse.objects.filter(user=request.user,course=course).exists():
            return Response({'error':'Course already exists in your list of courses'},status=status.HTTP_400_BAD_REQUEST)
        new_course = MyCourse.objects.create(user=request.user,course=course,bought_on=timezone.now())
        serializer = MyCourseSerializer(new_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
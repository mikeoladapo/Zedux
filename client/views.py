from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import MyCart,MyCourse
from .serializers import MyCartSerializer,MyCourse

class MyCartViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = MyCart.objects.filter(user=request.user)
        serializer = MyCartSerializer(queryset)
        return Response(serializer.data)
    def retrieve(self,request,pk):
        try:
            queryset = MyCart.objects.filter(pk=pk,user=request.user)
            serializer = MyCartSerializer(queryset,many=False)
            return Response(serializer.data)
        except MyCart.DoesNotExist:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    def create(self,request):
        serializer = MyCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def update(self,request,pk):
        queryset = MyCart.objects.filter(pk=pk,user=request.user)
        serializer = MyCartSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response()

    
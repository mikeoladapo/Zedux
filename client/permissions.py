from rest_framework.permissions import BasePermission
from .models import MyCart ,MyCourse

class IsMyOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view,obj):
        return request.user == obj.user 
    
class IsMyCart(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view,obj):
        return obj.user==request.user
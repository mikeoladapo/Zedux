from rest_framework.permissions import BasePermission
from .models import Course
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=="instructor" 
    
class IsCourseOwner(BasePermission):
    def has_permission(self, request, view,obj):
        return request.user == obj.instructor.use
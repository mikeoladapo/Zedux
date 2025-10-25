from django.contrib import admin
from .models import CustomUser,Instructor,Category,Course,CourseMaterial
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active']

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Instructor)
admin.site.register(Category)
admin.site.register(Course)
#admin.site.register(CourseMaterial)
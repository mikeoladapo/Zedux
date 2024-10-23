from django.contrib import admin
from .models import CustomUser,Instructor,Category,Course,CourseMaterial

admin.site.register(CustomUser)
admin.site.register(Instructor)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseMaterial)
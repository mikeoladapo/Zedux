from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        if not username:
            raise ValueError('The username must be set')
        if not password:
            raise ValueError('The password must be set')
        if not email:
            raise ValueError('The email address must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user 
    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('instructor',("student", "STUDENT"))
        return self.create_user(username,email,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Username validator logic
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_@#]+$',
        message="Username must contain letters, numbers, and underscores, @, and # only.",
        code="invalid_username"
    )

    def validate_username(value):
        if len(value) < 8:
            raise ValidationError("Username must not be less than 8 characters.")

    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[username_validator, validate_username]
    )

    email = models.EmailField(unique=True)  # same email cant be used multiple times 
    bio = models.TextField(blank=True, null=True)  
    role = models.CharField(max_length=100, choices=[("student", "STUDENT"), ("instructor", "INSTRUCTOR")],default=("student", "STUDENT"))
    date_joined = models.DateTimeField(default=timezone.now())
    profile_picture = models.ImageField(upload_to="profile_picture", blank=True, null=True)

    is_active = models.BooleanField(default=True)  # Required fields
    is_staff = models.BooleanField(default=False)  # Required for admin access

    objects = CustomUserManager()  # Assign the custom user manager

    USERNAME_FIELD = 'username'  # Required field
    REQUIRED_FIELDS = ['email']  # Other required fields

    def __str__(self):
        return self.username

   
class Instructor(models.Model):
    instructor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    bio = models.CharField(max_length=300)
    
    @property
    def instructor_name(self):
        return self.instructor.username
    
    def __str__(self):
        return self.instructor.username
    
class Category (models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name

class CourseMaterial(models.Model):
    video_file = models.FileField(upload_to="course_video",blank=True,null=True)
    certificate = models.FileField(upload_to="course_certificate",blank=True,null=True)
    other_file = models.FileField(upload_to="course_others",blank=True,null=True)
    text_file = models.TextField(blank=True,null=True)

 
    def __str__(self):
        return f"Course Material - {self.id}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    duration = models.DurationField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    course_material = models.ForeignKey(CourseMaterial,on_delete=models.CASCADE)

    @property
    def category_name(self):
        return self.category.name 
    @property
    def instructor_name(self):
        return self.instructor.username
    
    def __str__(self):
        return self.name 
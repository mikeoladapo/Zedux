from django.db import models
from django.contrib.auth.models import AbstractUser , Group ,Permission
from django.core.validators import RegexValidator ,MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password 
     
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #Validating the username using regex
    username_validator = RegexValidator(
        regex = r'^[a-zA-Z0-9_@#]+$',
        message = "username must contain letters , numbers and underscores,@,and # only",
        code = "Invalid username"
)
    # username validator logic 
    def validate_username(value):
        if len(value) < 8 :
            raise ValidationError("username must not be less than 8 digits")
        
    username  = models.CharField(max_length=20 ,validators=[username_validator,validate_username])

    password_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_@#]+$',
        message="password must contain letters , numbers and at least underscore,@,and # only",
        code = "The password is not strong enough"
    )

    password = models.CharField(max_length=200 ,validators=[MinLengthValidator(8,"password must not be less the 8"),password_validator])
    email = models.EmailField()
    bio = models.TextField()
    role = models.CharField(max_length=100 , choices=[("student","STUDENT"),("instructor","INSTRUCTOR")])
    joined_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to="profile_picture",blank=True,null=True) 
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True , null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True ,null=True)

    def save(self,*args,**kwargs):
        if self.id is None: # this hashes the password only when the user is been created
            self.set_password(self.password)
        super().save(*args,**kwargs)

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
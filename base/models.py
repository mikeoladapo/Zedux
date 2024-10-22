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
        regex = r'^[a-zA-Z0-9_]+$',
        message = "username must contain letters , numbers and underscores only",
        code = "Invalid username"
)
    # username validator logic 
    def validate_username(value):
        if len(value) < 8 :
            raise ValidationError("username must not be less than 8 digits")
        
    username  = models.CharField(max_length=20 ,validators=[username_validator,validate_username])

    password = models.CharField(max_length=18 ,validators=[MinLengthValidator(8,"password must not be less the 8")])
    email = models.EmailField()
    bio = models.TextField()
    role = models.CharField(max_length=100 , choices=[("student","STUDENT"),("instructor","INSTRUCTOR")])
    joined_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to="profile_picture",blank=True,null=True) 
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)


    def save(self,*args,**kwargs):
        if not self.id : # this hashes the password only when the user is been created
            self.password = make_password(self.password)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.username

   
class Instructor(models.Model):
    instructor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    bio = models.CharField(max_length=300)

class Category (models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name

class CourseMaterial(models.Model):
    text_file = models.FileField(upload_to="course_text",blank=True,null=True)
    video_file = models.FileField(upload_to="course_video",blank=True,null=True)
    certificate = models.FileField(upload_to="course_certificate",blank=True,null=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    duration = models.DurationField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    course_materials = models.ManyToManyField(CourseMaterial)



class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    def get_total_amount(self):
        total_amount = 0
        for course in self.courses.all():
            total_amount += course.amount
        return total_amount

class MyCourse(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    bought_on = models.DateTimeField()
    status = models.CharField(max_length=15,choices=[("completed","COMPLETED"),("in progress","IN PROGRESS"),("not started","NOT STARTED")])
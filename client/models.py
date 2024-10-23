from django.db import models
from base.models import CustomUser,Course 

class MyCart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    @property
    def user_name(self):
        return self.user.username
    @property
    def course_name(self):
        return self.course.name

class MyCourse(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    bought_on = models.DateTimeField()
    status = models.CharField(max_length=15,choices=[("completed","COMPLETED"),("in progress","IN PROGRESS"),("not started","NOT STARTED")])

    @property
    def user_name(self):
        return self.user.username
    @property
    def course_name(self):
        return self.course.name
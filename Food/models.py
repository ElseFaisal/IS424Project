from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Ceriricate table DB
class certificate(models.Model):
    courseid = models.AutoField(primary_key=True) # New Added
    cname = models.CharField(max_length=64)
    ccompany = models.CharField(max_length=64)
    users = models.ManyToManyField(User,blank=True,through="granted") # New Added , through means the new table in many-to-many relation
    
    def __str__(self):
        return f"Name: {self.cname} , Company: {self.ccompany}"

#New Added
class granted(models.Model):
    course = models.ForeignKey(certificate,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    grantedDate = models.DateField(null=True)
    
    def __str__(self):
        return f"Course Name: {self.courseName.cname} , Company: {self.courseName.ccompany} , UserName: {self.userName.username} , Granted Date: {self.grantedDate}"
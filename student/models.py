from django.db import models
from accounts.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20 , unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=15)

    image = models.ImageField(upload_to="media/img",blank=True, null=True)

    course = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    address = models.TextField()

    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    status = models.IntegerField(default=0)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"


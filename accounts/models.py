from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE =(
        ('admin','admin'),
        ('staff','staff'),
        ('student','student'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from accounts.models import User

class staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    address = models.TextField()
    status = models.IntegerField(default=0)
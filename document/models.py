from django.db import models
from student.models import Student

class StudentDocument(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE  , limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=100)
    discrip = models.TextField(max_length=300)
    doc = models.FileField(upload_to='doc/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default='pending'
    )

# Create your models here.

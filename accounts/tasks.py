from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def test_celery_task():
    print("✅ Celery task executed!")
    return "Task completed"

@shared_task
def send_welcome_email(email, first_name):
    subject = "Welcome to Student Management System"
    message = f"Hello {first_name},\n\nWelcome to our Student Management System! Your account has been created successfully."
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "Email sent successfully"

@shared_task
def send_notification_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False
    )
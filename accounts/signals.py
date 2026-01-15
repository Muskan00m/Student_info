from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from staff.models import staff
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from accounts.utils import generate_jwt


User = get_user_model()

@receiver(post_save, sender=User)
def create_related_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.role == "staff":
            staff.objects.get_or_create(user=instance)

@receiver(user_logged_in)
def create_jwt_on_google_login(request, user, **kwargs):
    tokens = generate_jwt(user)
    request.session['access_token'] = tokens['access']

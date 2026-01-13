from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from staff.models import staff
from accounts.utils import generate_jwt   

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.pk:  # new user
            user.role = 'staff'  # default role for Google login
            user.save()
            staff.objects.get_or_create(user = request.user)

        return user

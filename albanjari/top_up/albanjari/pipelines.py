from django.contrib.auth.models import Group
from .models import UserProfile

def create_user_profile(backend, user, response, *args, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if created:
        profile.role = 'PLAYER'  # Set default role or customize as needed
        profile.save()
        group_name = profile.role.capitalize()
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.clear()  # Clear existing groups if necessary
        user.groups.add(group)  # Add the new group
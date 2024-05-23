from .models import UserProfile

def add_user_profile_to_context(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    return {'user_profile': user_profile}

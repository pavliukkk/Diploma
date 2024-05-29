from .models import Reservation_main, UserProfile

def add_user_profile_to_context(request):
    user=request.user
    user_profile = None
    reservations = Reservation_main.objects.filter(user=user)
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    return {'reservations': reservations, 'user_profile': user_profile}

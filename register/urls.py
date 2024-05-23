# urls.py вашого додатку (наприклад, register)

from django.urls import path
from . import views

urlpatterns = [
    # Інші URL-шляхи вашого додатку
    path('save_user_data/', views.save_user_data, name='save_user_data'),
]

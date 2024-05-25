"""
URL configuration for kyrsova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.register, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('save-reservation/', save_reservation, name='save_reservation'),
    path('menu/', TemplateView.as_view(template_name='menu.html'), name='menu'),
    path('blogs/', TemplateView.as_view(template_name='blog.html'), name='blogs'),
    path('portfolio/', meal_list, name='portfolio'),
    path('save-reservation-meals/', save_reservation_meals, name='save_reservation_meals'),
    path('save_review/', save_review, name='save_review'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('blog-post/', TemplateView.as_view(template_name='blog-post.html'), name='blog-post'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('soon/', TemplateView.as_view(template_name='soon.html'), name='soon'),
    path('single-post/', TemplateView.as_view(template_name='single-post.html'), name='single-post'),
    path('profile/<str:username>/', profile_info, name='profile'),
    path('edit/<str:username>', profile_edit, name='profile_edit'),
    path('subscribe/', subscribe, name='subscribe'),
    path('switch_language/<str:language_code>/', views.switch_language, name='switch_language'),
    path('activate_page/', TemplateView.as_view(template_name='activate_page.html'), name='activate_page'),
    path('change_password/', change_password, name='change_password'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('send_activation_link/', views.activation_email_view, name='activation_email_view'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('login/activate/', views.send_activation_email, name='activate_account'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('make_reservation/', views.reservation_from_contact, name='make_reservation'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('change_avatar/', change_avatar, name='change_avatar'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('tables/', table_status, name='tables'),
    path('update_table_status/<int:table_id>/', update_table_status, name='update_table_status'),
    path('logout/', logout_view, name='logout'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


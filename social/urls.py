from django.urls import path
from . import views
from .forms import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'social'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
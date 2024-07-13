from django.urls import path
from . import views
from .forms import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'social'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('user/edit/', views.edit_user, name='edit_user'),
    path('ticket/', views.ticket, name='ticket'),

    path('posts/', views.post_list, name='post_list'),
    path('posts/detail/<int:id>', views.post_detail, name='post_detail'),
    path('posts/post/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
    path('posts/craete_post/', views.craete_post, name='craete_post'),
    path('search/', views.search, name='search'),
    path('posts/<post_id>/comment',views.post_comment,name='post_comment'),
    path('profile/', views.prof, name="profile"),


    # registration
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'),
                       name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
                       name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done'),
                       name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>',
                       auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
                       name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
                       name='password_reset_complete'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

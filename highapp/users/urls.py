from django.urls import path
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from .views import confirm_email, login, user_list, user_profile, user_edit_profile
from .forms import RegistrationForm

app_name = 'users'

urlpatterns = [
    path('confirm-email/<uuid:token>/', confirm_email, name='confirm-email'),
    path('accounts/register/', login, {'template_name': 'accounts/register.html', 'authentication_form': RegistrationForm}, name='register'),
    path('users/', user_list, name='user-list'),
    path('users/<str:username>/', user_profile, name='user-profile'),
    path('users/<str:username>/edit/', user_edit_profile, name='user-edit-profile'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html'),
         name='password_reset_form'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='reset_done'),
]
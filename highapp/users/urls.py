from django.urls import path, reverse_lazy
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       LoginView, LogoutView)

from .views import confirm_email, user_edit_profile, RegisterView, UserListView, user_profile


app_name = 'users'

urlpatterns = [
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', 
    confirm_email, name='activate'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('users/<str:username>/', user_profile, name='user-profile'),
    path('users/<str:username>/edit/', user_edit_profile, name='user-edit-profile'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html',
             success_url = reverse_lazy('users:password_change_done')),
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
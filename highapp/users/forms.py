from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string 

from .models import MyUser
from .token import account_activation_token 


class RegistrationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        message = render_to_string('acc_activate_email.html', { 
                'user': user, 
                'domain': '127.0.0.1:8000', 
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                'token':account_activation_token.make_token(user), 
            })
        send_mail(
            subject='Email confirmation',
            message=message,
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False,)
        return user


class UserEditForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        message = render_to_string('acc_activate_email.html', { 
                'user': user, 
                'domain': '127.0.0.1:8000', 
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                'token':account_activation_token.make_token(user), 
            })
        send_mail(
            subject='Email confirmation',
            message=message,
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False,)
        return user

from django import forms
from django.core.mail import send_mail

from .models import EmailConfirmation, MyUser


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        email_confirmation = EmailConfirmation.objects.create(user=user)
        send_mail(
            'Подтверждение электронной почты',
            'Пожалуйста, перейдите по ссылке для подтверждения вашей электронной почты.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email']
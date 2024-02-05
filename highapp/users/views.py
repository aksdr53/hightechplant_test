from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate

from .models import EmailConfirmation, MyUser
from .forms import RegistrationForm, UserEditForm


def confirm_email(request, token):
    email_confirmation = get_object_or_404(EmailConfirmation, token=token)
    email_confirmation.confirmed = True
    email_confirmation.save()
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_list(request):
    users = MyUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_profile(request, username):
    user = get_object_or_404(MyUser, username=username)
    return render(request, 'users/user_profile.html', {'user': user})

def user_edit_profile(request, username):
    user = get_object_or_404(MyUser, username=username)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            form.save()
            return redirect('user-profile', username=user.username)
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/user_edit_profile.html', {'form': form})

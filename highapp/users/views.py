from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .forms import RegistrationForm, UserEditForm
from .models import  MyUser
from .token import account_activation_token


def confirm_email(request, uidb64, token): 
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64)) 
        user = MyUser.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
    return redirect('users:home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:home')
    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})

def user_list(request):
    users = MyUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_profile(request, username):
    user = get_object_or_404(MyUser, username=username)
    current_user = request.user
    return render(request, 'users/user_detail.html', {'user': user, 'current_user': current_user})

@login_required
def user_edit_profile(request, username):
    user = get_object_or_404(MyUser, username=username)
    previous_email = user.email
    current_user = request.user
    if current_user != user:
        return redirect('users:user-profile', username=user.username)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            if user.email != previous_email:
                user.is_active = False
            form.save()
            return redirect('users:user-profile', username=user.username)
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/user_edit_profile.html', {'form': form, 'user': user})

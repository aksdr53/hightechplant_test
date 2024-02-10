from typing import Any
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm, UserEditForm
from .models import  MyUser
from .token import account_activation_token


class RegisterView(CreateView):
    template_name = 'users/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserListView(ListView):
    model = MyUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

@require_http_methods(["GET",])
def user_profile(request, username):
    """
    View function for displaying a user's profile.

    Retrieves a user with the given username from the database. If the user
    is not found, a 404 response is returned. The current authenticated user
    is also retrieved from the request object.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - username (str): The username of the user whose profile is to be displayed.

    Returns:
    - HttpResponse: A rendered HTML page displaying the user's profile.
    
    """
    user = get_object_or_404(MyUser, username=username)
    current_user = request.user
    return render(request, 'users/user_detail.html', {'user': user, 'current_user': current_user})

@require_http_methods(["GET", "POST"])
@login_required
def user_edit_profile(request, username):
    """This is a view function for editing a user's profile.

    This function handles both POST and GET requests. If it's a POST request
    the function checks the form validity and saves the changes to the user's profile.
    If it's a GET request, the function returns a form for editing the profile.

    :param request: HTTP request
    :type request: django.http.HttpRequest
    :param username: Username of the user whose profile needs to be edited
    :type username: str
    :return: Response to the request
    :rtype: django.http.HttpResponse
    """
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

@require_http_methods(["GET",])
def confirm_email(request, uidb64, token):
    """
    View function for confirming a user's email address based on a provided token.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - uidb64 (str): The base64-encoded user ID.
    - token (str): The activation token for email confirmation.

    Returns:
    - HttpResponse: Redirects the user to the 'users:home' URL after processing.

    """
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64)) 
        user = MyUser.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
    return redirect('users:home')
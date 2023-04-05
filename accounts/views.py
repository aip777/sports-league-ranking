from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

def login_view(request):
    """
    If logged in, redirects to dashboard, else redirects to log in page
    """
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('/team')
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # Authenticates using DefaultAuthenticationBackend
        user = authenticate(email=email, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'User Logged in Successfully !')
        return redirect('/team')
    context = {"form": form}
    return render(request, 'accounts/login.html', context)


def register_view(request):
    """
    If logged in, redirects to dashboard, else redirects to log in page
    """
    
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        messages.success(request, 'User Created Successfully !')
        return redirect('/team')
    
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    """ User Log out """
    logout(request)
    return redirect('')
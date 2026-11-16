from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    initial_role = request.GET.get('role', 'tenant')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to EasyBooking, {user.first_name or user.username}! Your account has been created.")
            if user.profile.role == 'owner':
                return redirect('owner_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below to register.")
    else:
        form = UserRegistrationForm(initial={'role': initial_role})

    return render(request, 'accounts/register.html', {'form': form, 'initial_role': initial_role})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if hasattr(user, 'profile') and user.profile.role == 'owner':
                    return redirect('owner_dashboard')
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, "Your profile was updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=user)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

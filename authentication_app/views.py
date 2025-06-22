#!/bin/pytthon3
import logging
import  re
from authentication_app.utilities.log_utils import ensure_daily_log_model_entry
from authentication_app.models import  User, SystemLogRecord
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
logger = logging.getLogger('shadowlink')

def userLogin(request):
    ensure_daily_log_model_entry()
    #checking if the user is logged in
    if request.user.is_authenticated:
        user_role = request.user.role
        request.session['user_role'] = user_role
        # logging the user login
        logger.info(f'User {request.user.username} logged in')
        return redirect('dashboard')
    else:
        # POST request for login
        if request.method == "POST":
            print('Trying login')
            userName = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=userName, password=password)
            if user is not None:
                #check for permission and redirect the user to their respective paths
                if user.role != 'ADMIN':
                    login(request, user)
                    logger.info(f'Login successful for username: {userName}')
                    messages.success(request, 'You have been logged in')
                    return redirect('dashboard')
                else: #if the role is admin then login the user and redirect the user to the admin site
                    login(request, user)
                    logger.info(f'Login successful for ADMIN: {userName}')
                    messages.success(request, 'Welcome Admin!')
                    return redirect('/admin/')  # or use reverse('admin:index')
            else:
                messages.error(request, 'Username or password is incorrect')
                logger.info(f'Login failed for username: {userName}')
                return redirect('login_page')
    return render(request, 'auth/login.html')

# method to check for password strength
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"\d", password) and
        re.search(r"[^\w\s]", password)  # special character
    )


def registerUser(request):
    ensure_daily_log_model_entry()
    if request.method == "POST":
        userName = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        profile_picture = request.FILES.get('profile_picture')
        role = "USER"

        # Check for missing fields
        if not userName or not email or not password:
            messages.error(request, "Username, email, and password are required.")
            logger.warning(f"Registration failed: Missing required fields.")
            return redirect('register_user')

        # Check password strength
        if not is_strong_password(password):
            messages.error(request,
                           "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")
            logger.warning(f"Registration failed for {userName}: Weak password.")
            return redirect('register_user')

        # Check for duplicate username/email
        if User.objects.filter(username=userName).exists():
            messages.error(request, "Username already taken.")
            logger.warning(f"Registration failed: Username {userName} already exists.")
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            logger.warning(f"Registration failed: Email {email} already exists.")
            return redirect('register_user')

        user = User.objects.create_user(
            username=userName,
            email=email,
            password=password,
            phone_number=phone_number,
            profile_picture=profile_picture,
            role=role
        )
        logger.info(f'User {userName} created successfully')
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login_page')
    return render(request, 'auth/register-user.html')

def userDashboard(request):
    return render(request, 'control/user-dashboard.html')
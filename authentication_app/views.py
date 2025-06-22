#!/bin/pytthon3
import logging
import  os
from authentication_app.utilities.log_utils import ensure_daily_log_model_entry
from django.conf import settings
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
            userName = request.POST.get("user-name")
            password = request.POST.get("password")
            user = authenticate(request, username=userName, password=password)
            if user is not None:
                #check for permission and redirect the user to their respective paths
                if user.role != 'ADMIN':
                    login(request, user)
                    logger.info(f'Login successful for username: {userName}')
                    messages.success(request, 'You have been logged in')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Username or password is incorrect')
                logger.info(f'Login failed for username: {userName}')
                return redirect('login_page')
    return render(request, 'auth/login.html')


def registerUser(request):

    return render(request, 'auth/register-user.html')

def userDashboard(request):
    return render(request, 'control/user-dashboard.html')
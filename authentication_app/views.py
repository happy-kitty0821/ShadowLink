#!/bin/pytthon3
import logging
import  re

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from authentication_app.utilities.log_utils import ensure_daily_log_model_entry
from authentication_app.models import  User, SystemLogRecord
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.signing import SignatureExpired, BadSignature, TimestampSigner
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

# user profile view
@login_required
def view_profile(request):
    context = {"user": request.user}
    return render(request, 'auth/user-profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        new_email = request.POST.get('email', user.email)
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        phone_number = request.POST.get('phone_number', user.phone_number)

        email_changed = False
        # email change logic
        if new_email != user.email:
            email_changed = True
            #check if new email already exists
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, "Email already exists, select a new one.")
                user.emails_verified = False  #mark email as unverified
                user.save()
                return redirect('update_profile')
            else:
                email_log_description = f"User {user.username} changed email from {user.email} to {new_email}."
                user.email = new_email
                user.emails_verified = False  #mark email as unverified

        # updating the other details
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()

        # logging the changes
        if email_changed:
            messages.warning(request, "Your email has been changed. Please verify it again.")
        else:
            messages.success(request, "Profile updated successfully.")

        return redirect('user_profile')

    return render(request, 'auth/update-profile.html', {'user': user})


@login_required
def verify_email(request):
    signer = TimestampSigner()
    # user's primary key ko anusar ma token singn and valid banako
    token = signer.sign(request.user.pk)
    # a full URL for email verification
    verification_url = request.build_absolute_uri(reverse('confirm_email')) + f'?token={token}'

    subject = "Verify Your Email Address"
    plain_message = f"Please verify your email address by clicking the link: {verification_url}"
    # render an HTML email template with the verification link
    html_message = render_to_string('email-templates/email-verify-link.html', {
        'user': request.user,
        'verification_url': verification_url,
    })

    # send the email
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [request.user.email], html_message=html_message)

    messages.info(request, "A verification email has been sent. Please check your inbox.")
    # return redirect('user_profile')
    return render(request, 'auth/user-profile.html')


def confirm_email(request):
    token = request.GET.get('token')
    if not token:
        messages.error(request, "Invalid or missing token.")
        return redirect('user_profile')

    signer = TimestampSigner()
    try:
        # dead after 10 mins
        user_pk = signer.unsign(token, max_age=360)
    except SignatureExpired:
        messages.error(request, "This verification link has expired.")
        return redirect('user_profile')
    except BadSignature:
        messages.error(request, "Invalid verification link.")
        return redirect('user_profile')

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_profile')

    user.emails_verified = True
    user.save()
    messages.success(request, "Your email has been successfully verified!")
    return redirect('user_profile')

# view to delete user account
@login_required
def userAccountDelete(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user

        #user password checking
        if user.check_password(password):
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('login')
        else:
            messages.error(request, "Password incorrect. Account not deleted.")
            return redirect('user_profile')
    else:
        return redirect('user_profile')
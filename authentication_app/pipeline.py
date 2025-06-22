from social_core.exceptions import AuthCanceled
from django.contrib import messages
from django.shortcuts import redirect

def social_auth_exception_handler(backend, strategy, request, response, *args, **kwargs):
    if response and response.get('error') == 'access_denied':
        messages.warning(request, "You canceled the login process.")
        return redirect('login_page')

from authentication_app import views as auth_views
from django.urls import path

urlpatterns = [
path('', auth_views.userLogin, name = 'login_page'),
]
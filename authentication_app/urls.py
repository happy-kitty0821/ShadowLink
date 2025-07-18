from authentication_app import views as auth_views
from django.urls import path
from django.contrib.auth import views as pwChangeViews #using django's default pw reset classes
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', auth_views.userLogin, name = 'login_page'),
    path('register-user', auth_views.registerUser, name = 'register_user'),
    path('user-profile', auth_views.view_profile, name = 'user_profile'),
    path('user-profile/update', auth_views.update_profile, name = 'update_profile'),
    path('user-profile/verify-email', auth_views.verify_email, name = 'verify_email'),
    path('profile/confirm-email/', auth_views.confirm_email, name='confirm_email'),
    path('user-profile/delete/account', auth_views.userAccountDelete, name = 'delete_account' ),
    #user logout view
    path('logout/', LogoutView.as_view(), name='logout'),

    #password reset flow
    path('reset-password/', pwChangeViews.PasswordResetView.as_view(template_name='auth/reset-password.html'),
         name='password-reset'),
    path('reset-password-done/', pwChangeViews.PasswordResetDoneView.as_view(template_name='auth/reset-done.html'),
         name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/',
         pwChangeViews.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         pwChangeViews.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'),
         name='password_reset_complete'),

    #password change flow
    path('change-password/', pwChangeViews.PasswordChangeView.as_view(template_name='auth/change-password.html'),
         name='password_change'),
    path('change-password-done/',
         pwChangeViews.PasswordChangeDoneView.as_view(template_name='auth/change-password-done.html'),
         name='password_change_done'),
]
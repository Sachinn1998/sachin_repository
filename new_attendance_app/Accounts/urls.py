from django.urls import path,include
from Accounts import views
from django.contrib.auth import views as auth_viwes

urlpatterns = [
    path('login/homepage/',views.home_page),
    path('logout/',views.logout_page),
    path('accounts/',include('django.contrib.auth.urls')),
    path('sign_up/',views.sign_up),
    path('login/',views.login),
    path('change_pwd/',views.change_password),
    path('reset_password/',auth_viwes.PasswordResetView.as_view(template_name='registration/reset_password.html'), name='reset_password'),
    path('reset_password_sent/',auth_viwes.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('rest/<uidb64>/<token>',auth_viwes.PasswordResetConfirmView.as_view(template_name='registration/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/',auth_viwes.PasswordResetCompleteView.as_view(template_name='registration/reset_password_done.html'), name='password_reset_complete'),
]

from django.urls import path
from . import views

urlpatterns = [
        path('register/start/', views.start, name='start'),
        path('register/login/', views.login, name='login'),
        path('register/register_form/', views.register_form, name='register_form'),
        path('register/home/', views.home, name='home'),
        path('register/otp_ver/', views.otp_ver, name='otp_ver'),
        path('register/forget_password/', views.forget_password, name='forget_password'),
        path('register/reset_password/', views.reset_password, name='reset_password')
]

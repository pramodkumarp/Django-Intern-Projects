from django.urls import path
from BlogApp import views


urlpatterns = [
    path('user/register/', views.signup, name="signup"),
    path('user/skip_uploading_image/<slug:name>/', views.skip_uploading_image, name="skip_uploading_image"),
    path('user/resend_code/<slug:name>/', views.resend_verification_code, name="resend_verification_code"),
    path('user/login/', views.login, name="login"),
    path('user/logout/', views.logout, name="logout"),
    path('user/profile/', views.profile, name="profile"),
]
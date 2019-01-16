from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.loging),
    path('user/logged-in/dashboard/', views.dashboard),
]
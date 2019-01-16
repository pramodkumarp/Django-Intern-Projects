from django.urls import path
from . import views

urlpatterns = [
    path('', views.email),
    path('success/', views.success),
]
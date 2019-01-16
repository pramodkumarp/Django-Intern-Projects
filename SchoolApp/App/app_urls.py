from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create_new_user/', views.create_new_user),
    path('add_user/', views.add_user),
    path('edit_user/<int:id>', views.edit_user),
    path('edit/<int:id>', views.edit),
    path('user_details/<int:id>', views.user_details),
    path('delete/<int:id>', views.delete),
]
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index),
    path('upload/', views.upload),
    path('edit/<id>', views.edit),
    path('update/<id>', views.update),
    path('delete/<id>', views.delete),
]
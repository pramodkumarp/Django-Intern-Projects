from django.urls import path
from . import views



urlpatterns = [
    path('', views.home),
    path('user/create_page/', views.create_page),
    path('user/create/', views.create),
    path('user/details_page/<id>', views.details_page),
    path('user/edit_page/<id>', views.edit_page),
    path('user/update/<id>', views.update),
    path('user/delete/<id>', views.delete),
]
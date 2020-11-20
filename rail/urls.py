from django.urls import path
from . import views

urlpatterns = [
    path('add_train', views.add_train), 
]
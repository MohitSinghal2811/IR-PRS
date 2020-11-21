from django.urls import path
from . import views

urlpatterns = [
    path('add_train', views.add_train), 
    path('add_released_train', views.add_released_train),
    path('', views.index, name = 'index'),
    path('login', views.userlogin, name = 'login'),
    path('register', views.register, name = 'register'), 
    path('logout', views.userlogout, name = 'logout'),
]
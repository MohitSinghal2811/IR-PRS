from django.urls import path
from . import views

urlpatterns = [
    path('add_train', views.add_train), 
    path('add_released_train', views.add_released_train),
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('signup', views.signup, name = 'signup'), 
    path('logout', views.logout, name = 'logout'),
]
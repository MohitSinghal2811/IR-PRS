from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home, name = 'home'),
    path('find_train', views.find_train, name = 'find_train'),
    path('reservation', views.reservation, name = 'reservation'),
    path('profile', views.profile, name = 'profile'),
    path('booking_history', views.booking_history ,  name = 'booking_history'),


    path('add_train', views.add_train), 
    # path('add_released_train', views.add_released_train),
    path('', views.index, name = 'index'),
    path('login', views.userlogin, name = 'login'),
    path('register', views.register, name = 'register'), 
    path('logout', views.userlogout, name = 'logout'),
    path('release_train', views.releaseTrain, name = 'release_train'),

    path('helper', views.helper, name = 'helper'),
    path('booking/<int:releasedTrainId>', views.booking, name = 'booking'),
    # path('booking', views.booking, name = 'booking')
]
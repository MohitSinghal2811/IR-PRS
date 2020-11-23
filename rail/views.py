from django.shortcuts import render

from .forms import TrainForm, LoginForm, RegisterForm, ReleasedTrainForm
from django.contrib.auth import authenticate, login, logout
from .models import Train, BookingAgent
from django.contrib.auth.models import User


def add_train(request):
    if request.method == 'POST':
        print(request.POST)
        form = TrainForm(request.POST)
        if form.is_valid():
            train = Train(trainNumber = request.POST.get('trainNumber'), starts = request.POST.get('starts'), ends = request.POST.get('ends'), name = request.POST.get('name'))
            train.save()
    else:
        form = TrainForm()
    return render(request, 'rail/add_train.html', {'form': form})


def add_released_train(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReleasedTrainForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ReleasedTrainForm()
    return render(request, 'rail/add_released_train.html', {'form': form})
    



def index(request):
    return render(request, 'rail/index.html')

def home(request):
    return render(request, 'rail/index.html')

def find_train(request):
    return render(request, 'rail/index.html')

def reservation(request):
    return render(request, 'rail/index.html')

def profile(request):
    return render(request, 'rail/index.html')

def booking_history(request):
    return render(request, 'rail/index.html')



def userlogin(request):
    showError = False
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            var = authenticate(request, username =  request.POST.get('username'), password = request.POST.get('password'))
            if(var is None):
                showError = True
            else:
                login(request, var)
                return render(request, 'rail/index.html')
        else:
            showError = True
    else:
        form = LoginForm()
    return render(request, 'rail/login.html', {'form' : form, 'showError' : showError})

def register(request):
    showError = False
    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = request.POST.get('username'), email = request.POST.get('email'), password = request.POST.get('password'))
            bookingAgent = BookingAgent(user = user, name = request.POST.get('name'), creditCardNo = request.POST.get('creditCardNo'), address = request.POST.get('address'), age = request.POST.get('age'), gender = request.POST.get('gender'), email = request.POST.get('email'))
            bookingAgent.save()
            var = authenticate(request, username =  request.POST.get('username'), password = request.POST.get('password'))
            login(request, var)
            return render(request, 'rail/index.html')
        else :
            showError = True
    else:
        form = RegisterForm()
    return render(request, 'rail/register.html', {'form': form, 'showError' : showError})

def userlogout(request):
    logout(request)
    return render(request, 'rail/index.html')


def releaseTrain(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReleasedTrainForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ReleasedTrainForm()
    return render(request, 'rail/release_train.html', {'form':form} )
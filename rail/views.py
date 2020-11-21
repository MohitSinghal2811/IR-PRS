from django.shortcuts import render

from .forms import TrainForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def add_train(request):
    if request.method == 'POST':
        print(request.POST)
        form = TrainForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TrainForm()
    return render(request, 'rail/add_train.html', {'form': form})


def add_released_train(request):
    pass



def index(request):
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
    return render(request, 'rail/signup.html')

def userlogout(request):
    logout(request)
    return render(request, 'rail/index.html')
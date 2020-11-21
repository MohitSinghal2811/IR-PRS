from django.shortcuts import render

from .forms import TrainForm

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


def login(request):
    return render(request, 'rail/login.html')

def signup(request):
    return render(request, 'rail/signup.html')

def logout(request):
    pass
from django.shortcuts import render, redirect

from .forms import TrainForm, LoginForm, RegisterForm, ReleasedTrainForm, PassengerForm, TicketForm, BasePassengerFormSet,FindTrainForm
from django.contrib.auth import authenticate, login, logout
from .models import Train, BookingAgent, ReleasedTrain, Berth, Seat, Coach, Passenger, Books, Pnr
from django.contrib.auth.models import User
from .helper_functions import berthTableCreator, trainsCreator
import datetime
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import Http404
from .helper_functions import berthExtractor, coachExtractor



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


def index(request):
    return render(request, 'rail/index.html')

def home(request):
    return render(request, 'rail/index.html')


def reservation(request):
    return render(request, 'rail/reservation.html')

def profile(request):
    return render(request, 'rail/profile.html')

def booking_history(request):
    if request.POST.get('user')=='':
        pass
    else:
        ba=BookingAgent.objects.filter(user = request.POST.get('user'))
        all_pnr=Pnr.objects.filter(bookingAgent=ba)

        return render(request, 'rail/booking_history.html' , {'all_pnr' : all_pnr})



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


def find_train(request):
    showError=False
    display=[]
    if request.method=='POST':
        print(request.POST)
        form = FindTrainForm(request.POST)
        if form.is_valid():
            s=request.POST.get('source')
            d=request.POST.get('destination')
            trains=Train.objects.filter(starts=s ).filter(ends=d)
            print(trains)
            for train in trains:
                print(train)
                results=ReleasedTrain.objects.filter(train=train)
                for res in results:
                    if res.departureDate>=datetime.date.today() and res.departureTime>= datetime.datetime.now().time():
                        display.append(res)
                        print(res)              
        else:
            showError=True
    else:
        form=FindTrainForm()
    return render(request , 'rail/find_train.html' , {'form' : form ,'showEroor' : showError , 'display' :display})



def userlogout(request):
    logout(request)
    return redirect('/home')


def releaseTrain(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReleasedTrainForm(request.POST)
        if form.is_valid():
            train = Train.objects.filter(trainNumber = request.POST.get("trainNumber"))[0]
            var = ReleasedTrain(train = train, departureDate = request.POST.get("departureDate") , departureTime = request.POST.get("departureTime"), maxAC = int(request.POST.get("acCoachNo")) * 18, maxSL = int(request.POST.get("slCoachNo")) * 24, currAC = 1, currSL = 1, releasedDate = datetime.date.today(), releasedTime = datetime.datetime.now().time())
            var.save()
            for i in range(1, int(request.POST.get('acCoachNo')) + 1):
                coach = Coach(releasedTrain = var, coachType = "AC", coachNumber = i)
                coach.save()
            for i in range(1, int(request.POST.get('slCoachNo')) + 1):
                coach = Coach(releasedTrain = var, coachType = "SL", coachNumber = i)
                coach.save()
            return render(request, 'rail/index.html')
    else:
        form = ReleasedTrainForm()
    return render(request, 'rail/release_train.html', {'form':form} )




def booking(request, releasedTrainId):
    releasedTrain = ReleasedTrain.objects.filter(pk = releasedTrainId)
    if(request.user.is_anonymous):
        return redirect('/login')
    if(releasedTrain.count() == 0):
        raise Http404("Page not Found")
    releasedTrain = releasedTrain[0]
    PassengerFormSet = formset_factory(PassengerForm, formset=BasePassengerFormSet)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST)
        if ticket_form.is_valid() and passenger_formset.is_valid():
            if(len(passenger_formset) > 6):
                errorMessage = "You can only book a maximum of 6 tickets at a time"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage })
            if(ticket_form.cleaned_data.get('coachType') == "AC" and len(passenger_formset) > releasedTrain.maxAC - releasedTrain.currAC + 1):
                errorMessage = "Not enough seats available in this class"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage })
            if(ticket_form.cleaned_data.get('coachType') == "SL" and len(passenger_formset) > releasedTrain.maxSL - releasedTrain.currSL + 1):
                errorMessage = "Not enough seats available in this class"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage })
            for passenger_form in passenger_formset:
                name = passenger_form.cleaned_data.get('name')
                age = passenger_form.cleaned_data.get('age')
                gender = passenger_form.cleaned_data.get('gender')
                if name and age and gender:
                    passenger = Passenger(name = name, age = age, gender = gender)
                    passenger.save()
                    bookingAgent = BookingAgent.objects.filter(user = request.user)[0]
                    bookingAgent.save()
                    pnr = Pnr(bookingAgent = bookingAgent)
                    pnr.save()
                    seat = Seat( berth = berthExtractor(releasedTrain, ticket_form.cleaned_data.get('coachType')),coach = coachExtractor(releasedTrain, ticket_form.cleaned_data.get('coachType')))
                    seat.save()
                    books = Books(seat = seat, passenger = passenger, pnr = pnr)
                    books.save()
        return redirect('/home')    
    else:
        ticket_form = TicketForm()
        passenger_formset = PassengerFormSet()
    return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain })








# def helper(request):
#     trainsCreator()
#     return render(request, 'rail/index.html')

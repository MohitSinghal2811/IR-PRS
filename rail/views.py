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
    if(not request.user.is_superuser):
        return redirect('/login')
    if request.method == 'POST':
        print(request.POST)
        form = TrainForm(request.POST)
        if form.is_valid():
            train = Train(trainNumber = request.POST.get('trainNumber'), starts = request.POST.get('starts'), ends = request.POST.get('ends'), name = request.POST.get('name'), admin = request.user)
            train.save()
        return redirect('/home')
    else:
        form = TrainForm()
    return render(request, 'rail/add_train.html', {'form': form})


def index(request):
    return redirect('/home')

def home(request):
    return render(request, 'rail/index.html')

def ticket_details(request, pnrno):
    if(request.user.is_anonymous):
        return redirect('/login')
    pnr = Pnr.objects.filter(id = pnrno)
    if(pnr.count() == 0):
        raise Http404("Page not Found")
    pnr = pnr[0]
    tickets2 = Books.objects.filter(pnr = pnr)
    ticket = tickets2[0]
    seat = ticket.seat
    coach = seat.coach
    releasedTrain = coach.releasedTrain
    total_fare=0
    if coach.coachType=='AC':
        base_fare= coach.releasedTrain.fareAC
    else:
        base_fare= coach.releasedTrain.fareSL
    fares=[]
    print(releasedTrain)
    print(tickets2)
    for p in tickets2:
        print(p.passenger.gender)
        print(p.passenger.age)
        if p.passenger.gender=='M' and p.passenger.age>60 :
            fares.append((0.6)*base_fare)
            total_fare=total_fare + (0.6)*base_fare
        elif p.passenger.gender=='F' and p.passenger.age>58 :
            fares.append((0.5)*base_fare)
            total_fare=total_fare + (0.5)*base_fare
        else:
            fares.append(base_fare)
            total_fare=total_fare+base_fare
    
    tickets = zip(tickets2, fares)
    return render(request, 'rail/ticket_details.html', {'releasedTrain':releasedTrain, 'tickets' : tickets, 'pnrno':pnrno, 'total_fare':total_fare})

def reservation(request):
    return redirect('/find_train')

def profile(request):
    return render(request, 'rail/profile.html')

def booking_history(request, uname):
    if(request.user.is_anonymous):
        return redirect('/login')
    else:
        ba=BookingAgent.objects.filter(user = request.user)
        if(ba.count() == 0):
            raise Http404("Page not Found")
        ba = ba[0]
        all_pnr = Pnr.objects.filter(bookingAgent=ba)
        print(all_pnr)
        print(all_pnr.count())
        releasedTrains = []
        fares=[]
        if(all_pnr):
            for pnr in all_pnr:
                total_fare = 0
                detail = {}
                ticket = Books.objects.filter(pnr = pnr)[0]
                print(ticket)
                seat = ticket.seat
                print(seat)
                coach = seat.coach
                releasedTrains.append(coach.releasedTrain)
                if coach.coachType=='AC':
                    base_fare= coach.releasedTrain.fareAC
                else:
                    base_fare= coach.releasedTrain.fareSL

                all_pass=Books.objects.filter(pnr = pnr)
                print(all_pass)
                for p in all_pass:
                    print(p.passenger.gender)
                    print(p.passenger.age)
                    if p.passenger.gender=='M' and p.passenger.age>60 :
                        total_fare=total_fare + (0.6)*base_fare
                    elif p.passenger.gender=='F' and p.passenger.age>58 :
                        total_fare=total_fare + (0.5)*base_fare
                    else:
                        total_fare=total_fare+base_fare
                
                fares.append(total_fare)
        details = zip(all_pnr, releasedTrains ,fares)
        return render(request, 'rail/booking_history.html' , {'details' : details })



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
                return redirect('/home')
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
            user.first_name = form.cleaned_data.get('name')
            user.save()
            bookingAgent = BookingAgent(user = user, name = request.POST.get('name'), creditCardNo = request.POST.get('creditCardNo'), address = request.POST.get('address'), dob = form.cleaned_data.get('dob'), gender = request.POST.get('gender'), email = request.POST.get('email'))
            bookingAgent.save()
            var = authenticate(request, username =  request.POST.get('username'), password = request.POST.get('password'))
            login(request, var)
            return redirect('/home')
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
            date=form.cleaned_data.get('Date')
            trains=Train.objects
            if s!='':
                trains=trains.filter(starts=s )
            if d!='':  
                trains=trains.filter(ends=d)
            print("HI")
            print(trains)           
            if(date is None):
                print("if 1")
                for train in trains:
                    print(train)
                    results=ReleasedTrain.objects.filter(train=train)
                    for res in results:
                        print("HIII")
                        # if res.departureDate>=datetime.date.today() and res.departureTime>= datetime.datetime.now().time():
                        #     print("HHHH")
                        #     display.append(res)
                        #     print(res)
                        display.append(res)
                        print(res)
            else:
                print("if 2")
                for train in trains:
                    print(train)
                    results=ReleasedTrain.objects.filter(train=train)
                    for res in results:
                        print(res.departureDate)
                        print(date)
                        print(res.departureDate==date)
                        if res.departureDate==date:
                            
                            display.append(res)
                            print(res)
        else:
            showError=True
    else:
        form=FindTrainForm()
    print(display)
    return render(request , 'rail/find_train.html' , {'form' : form ,'showError' : showError , 'display' :display})



def userlogout(request):
    logout(request)
    return redirect('/home')


def releaseTrain(request):
    if(not request.user.is_superuser):
        return redirect('/login')
    if request.method == 'POST':
        print(request.POST)
        form = ReleasedTrainForm(request.POST)
        if form.is_valid():
            train = Train.objects.filter(trainNumber = request.POST.get("trainNumber"))[0]
            print(request.POST)
            var = ReleasedTrain(train = train, departureDate = request.POST.get("departureDate") , departureTime = request.POST.get("departureTime"), maxAC = int(request.POST.get("acCoachNo")) * 18, maxSL = int(request.POST.get("slCoachNo")) * 24, currAC = 1, currSL = 1, releasedDate = datetime.date.today(), releasedTime = datetime.datetime.now().time(), admin = request.user, fareAC = form.cleaned_data.get('fareac'), fareSL = form.cleaned_data.get('faresl'))
            var.save()
            for i in range(1, int(request.POST.get('acCoachNo')) + 1):
                coach = Coach(releasedTrain = var, coachType = "AC", coachNumber = i)
                coach.save()
            for i in range(1, int(request.POST.get('slCoachNo')) + 1):
                coach = Coach(releasedTrain = var, coachType = "SL", coachNumber = i)
                coach.save()
            return redirect('/home')
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
    print(releasedTrain)
    acavailable = releasedTrain.maxAC - releasedTrain.currAC + 1
    slavailable = releasedTrain.maxSL - releasedTrain.currSL + 1
    slfare = releasedTrain.fareSL
    acfare = releasedTrain.fareAC
    PassengerFormSet = formset_factory(PassengerForm, formset=BasePassengerFormSet, extra = 1)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST)

        print(ticket_form.is_valid())
        print(passenger_formset.is_valid())
        if ticket_form.is_valid() and passenger_formset.is_valid():
            print("is-valid")
            if(len(passenger_formset) <= 0):
                ticket_form = TicketForm()
                passenger_formset = PassengerFormSet()
                errorMessage = "There should be atleast one passenger"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage, 'acavailable':acavailable , 'slavailable' : slavailable , 'acfare': acfare, 'slfare' : slfare})
            if(len(passenger_formset) > 6):
                errorMessage = "You can only book a maximum of 6 tickets at a time"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage, 'acavailable':acavailable , 'slavailable' : slavailable, 'acfare': acfare, 'slfare' : slfare })
            if(ticket_form.cleaned_data.get('coachType') == "AC" and len(passenger_formset) > releasedTrain.maxAC - releasedTrain.currAC + 1):
                errorMessage = "Not enough seats available in this class"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage, 'acavailable':acavailable , 'slavailable' : slavailable, 'acfare': acfare, 'slfare' : slfare })
            if(ticket_form.cleaned_data.get('coachType') == "SL" and len(passenger_formset) > releasedTrain.maxSL - releasedTrain.currSL + 1):
                errorMessage = "Not enough seats available in this class"
                return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain, 'errorMessage': errorMessage, 'acavailable':acavailable , 'slavailable' : slavailable, 'acfare': acfare, 'slfare' : slfare })
            bookingAgent = BookingAgent.objects.filter(user = request.user)[0]
                    
            pnr = Pnr(bookingAgent = bookingAgent)
            pnr.save()
            
            for passenger_form in passenger_formset:

                name = passenger_form.cleaned_data.get('name')
                age = passenger_form.cleaned_data.get('age')
                gender = passenger_form.cleaned_data.get('gender')
                aadhar = passenger_form.cleaned_data.get('aadhar')
                if name and age and gender and aadhar:
                    var = Passenger.objects.filter(aadhar = aadhar)
                    if(var.count() == 1):
                        passenger = var[0]
                        passenger.name = name
                        passenger.age = age
                        passenger.gender = gender
                        passenger.save()
                    else:
                        passenger = Passenger(aadhar = aadhar ,name = name, age = age, gender = gender)
                        passenger.save()

                    print(name)
                    print("here")
                    seat = Seat( berth = berthExtractor(releasedTrain, ticket_form.cleaned_data.get('coachType')),coach = coachExtractor(releasedTrain, ticket_form.cleaned_data.get('coachType')))
                    seat.save()
                    books = Books(seat = seat, passenger = passenger, pnr = pnr)
                    books.save()

            return redirect('/ticket/{}'.format(pnr.id))    
    else:
        ticket_form = TicketForm()
        passenger_formset = PassengerFormSet()

        
    return render(request, 'rail/booking.html', context = {'ticket_form': ticket_form,'passenger_formset': passenger_formset, 'releasedTrain': releasedTrain , 'acavailable':acavailable , 'slavailable' : slavailable, 'acfare': acfare, 'slfare' : slfare})








def helper(request):
    berthTableCreator()
    return render(request, 'rail/index.html')

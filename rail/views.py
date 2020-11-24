from django.shortcuts import render, redirect

from .forms import TrainForm, LoginForm, RegisterForm, ReleasedTrainForm, PassengerForm, TicketForm, BasePassengerFormSet,FindTrainForm
from django.contrib.auth import authenticate, login, logout
from .models import Train, BookingAgent, ReleasedTrain, Berth, Seat, Coach, Passenger, Books, Pnr
from django.contrib.auth.models import User
from .helper_functions import berthTableCreator, trainsCreator
import datetime
from django.forms.formsets import formset_factory


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


def reservation(request):
    return render(request, 'rail/reservation.html')

def profile(request):
    return render(request, 'rail/profile.html')

def booking_history(request):
    return render(request, 'rail/booking_history.html')



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
    return render(request, 'rail/index.html')


def releaseTrain(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReleasedTrainForm(request.POST)
        if form.is_valid():
            train = Train.objects.filter(trainNumber = request.POST.get("trainNumber"))[0]
            var = ReleasedTrain(train = train, departureDate = request.POST.get("departureDate") , departureTime = request.POST.get("departureTime"), maxAC = int(request.POST.get("acCoachNo")) * 18, maxSL = int(request.POST.get("slCoachNo")) * 24, currAC = 1, currSL = 1, releasedDate = datetime.date.today(), releasedTime = datetime.datetime.now().time())
            var.save()
            return render(request, 'rail/index.html')
    else:
        form = ReleasedTrainForm()
    return render(request, 'rail/release_train.html', {'form':form} )




def booking(request):
    
    # Create the formset, specifying the form and formset we want to use.
    PassengerFormSet = formset_factory(PassengerForm, formset=BasePassengerFormSet)

    # Get our existing link data for this user.  This is used as initial data.
    # user_links = UserLink.objects.filter(user=user).order_by('anchor')
    # link_data = [{'anchor': l.anchor, 'url': l.url}
                    # for l in user_links]

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST)

        if ticket_form.is_valid() and passenger_formset.is_valid():
            # Save user info
            # user.first_name = profile_form.cleaned_data.get('first_name')
            # user.last_name = profile_form.cleaned_data.get('last_name')
            # user.save()

            # Now save the data for each form in the formset
            new_passengers = []

            for passenger_form in passenger_formset:
                name = passenger_form.cleaned_data.get('name')
                age = passenger_form.cleaned_data.get('age')
                gender = passenger_form.cleaned_data.get('gender')

                if name and age and gender:
                    new_passengers.append(Passenger(name = name, age = age, gender = gender))

            # try:
            #     with transaction.atomic():
            #         #Replace the old with the new
            #         UserLink.objects.filter(user=user).delete()
            #         UserLink.objects.bulk_create(new_links)

            #         # And notify our users that it worked
            #         messages.success(request, 'You have updated your profile.')

            # except IntegrityError: #If the transaction failed
            #     messages.error(request, 'There was an error saving your profile.')
            #     return redirect(reverse('profile-settings'))

    else:
        ticket_form = TicketForm()
        passenger_formset = PassengerFormSet()

    context = {
        'ticket_form': ticket_form,
        'passenger_formset': passenger_formset,
    }

    return render(request, 'rail/booking.html', context)








def helper(request):
    trainsCreator()
    return render(request, 'rail/index.html')

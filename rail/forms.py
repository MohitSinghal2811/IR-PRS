from django import forms
from .validators import isTrainNumberUnique, isCreditCardNumberUnique, isEmailUnique, isUserNameUnique, isDepartureDateValid, trainExists
import django.contrib.admin.widgets as widgets
from .my_widgets import MyDateWidget, MyTimeWidget, MyTestWidget
from .models import ReleasedTrain, Train
import datetime
from django.forms.formsets import BaseFormSet



class TrainForm(forms.Form):
    trainNumber = forms.IntegerField(help_text= "Train number should be of 4-5 characters and should be unique", widget = forms.NumberInput(attrs={'placeholder' :"Train Number",  'required': True , 'autofocus' : True}), max_value=99999, min_value=1000, validators = [isTrainNumberUnique, ], label = 'Train Number')
    starts = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={'placeholder' :"Start Station",  'required': True }), label = 'Source')
    ends = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={'placeholder' :"Destination",  'required': True }), label = 'Destination')
    name = forms.CharField(max_length = 30, widget = forms.TextInput(attrs={'placeholder' :"Train Name", 'required': True }), label = 'Name of the Train')


    def clean(self):
        super(TrainForm, self).clean()
        starts = self.cleaned_data.get('starts')
        ends = self.cleaned_data.get('ends')
        if(starts == ends):
            raise forms.ValidationError('Source and Destination must be different')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'placeholder' :"Username",  'required': True , 'autofocus' : True}), label = "User Name")
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder' :"Password",  'required': True}), label = "Password")

class find_train(forms.Form):
    Source = forms.CharField(max_length = 30, widget = forms.TextInput(attrs={'placeholder' :"Source", 'required': True }), label = 'Source')

    destination =forms.CharField(max_length = 30, widget = forms.TextInput(attrs={'placeholder' :"Destination", 'required': True }), label = 'Destination')

    

class RegisterForm(forms.Form):
    GENDER_CHOICES = (
        ("M", "Male"), 
        ("F", "Female"), 
        ("O", "Other"),
    )

    username = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'placeholder' :"Username",  'required': True , 'autofocus' : True}), label = "User Name", help_text = "Username should be unique", validators = [isUserNameUnique, ])
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder' :"Password",  'required': True}), label = "Password")
    name = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'placeholder' :"Full Name",  'required': True}), label = "Full Name")
    email = forms.EmailField(widget = forms.EmailInput(attrs={'placeholder' :"Email Address",  'required': True}), label = "Email Address", validators = [isEmailUnique, ])
    creditCardNo = forms.IntegerField(max_value=99999999999999, min_value=10000000000000, widget = forms.TextInput(attrs={'placeholder' :"Credit Card Number",  'required': True}), label = "Credit Card Number", validators = [isCreditCardNumberUnique, ], help_text = "Credit Card Number is of 14 digits")
    address = forms.CharField(max_length=200, widget = forms.TextInput(attrs={'placeholder' :"Address",  'required': True}), label = "Address")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget = forms.Select(attrs={'placeholder' :"Gender",  'required': True}), label = "Gender")
    age = forms.IntegerField(min_value=16, max_value=200, widget = forms.NumberInput(attrs={'placeholder' :"Age",  'required': True}), label = "Age")

class ReleasedTrainForm(forms.Form):
    trainNumber = forms.IntegerField( widget = forms.TextInput(attrs={'placeholder' :"Train Number",  'required': True , 'autofocus' : True , 'class' : "form-control"}), max_value=99999, min_value=1000, validators = [trainExists, ], label = 'Train Number')
    departureDate = forms.DateField(label = "Departure Date", widget = forms.DateInput(attrs={'required' : True}), validators = [isDepartureDateValid, ])
    departureTime = forms.TimeField(label = "Departure Time", widget = forms.TimeInput(attrs={'required' : True}))
    acCoachNo = forms.IntegerField(min_value=0, widget = forms.NumberInput(attrs={'placeholder' :"Number of Ac Coaches",'class' : "form-control",  'required': True}), label = "Number of Ac Coaches", initial = 0)
    slCoachNo = forms.IntegerField(min_value=0, widget = forms.NumberInput(attrs={'placeholder' :"Number of Sleeper Coaches", 'class' : "form-control",  'required': True}), label = "Number of Sleeper Coaches", initial = 0)


    def clean(self):
        super(ReleasedTrainForm, self).clean()
        val = False
        if(self.cleaned_data.get('departureDate') != "" and self.cleaned_data.get('departureTime') != "" and self.cleaned_data.get('trainNumber') != ""):
            departureDate = self.cleaned_data.get('departureDate')
            departureTime = self.cleaned_data.get('departureTime')
            train = Train.objects.filter(trainNumber = self.cleaned_data.get('trainNumber'))
            if(train.count() != 0):
                train = train[0]
                var = ReleasedTrain.objects.filter(train = train).filter(departureDate = departureDate).filter(departureTime = departureTime)
                if(var.count() != 0):
                    val = True
                    self.add_error('trainNumber', "This train has already been released at this date and time")
                    self.add_error('departureDate', "This train has already been released at this date and time")
                    self.add_error('departureTime', "This train has already been released at this date and time")
        acCoachNo = self.cleaned_data.get('acCoachNo')
        slCoachNo = self.cleaned_data.get('slCoachNo')
        if(acCoachNo + slCoachNo > 28 or acCoachNo + slCoachNo <= 0):
            self.add_error('acCoachNo', "Total Number of Coaches should be less than 28 and greater than 0")
            self.add_error('slCoachNo', "Total Number of Coaches should be less than 28 and greater than 0")
            val = True

        if(val == True):
            raise forms.ValidationError("Details are Incorrect")

    

class PassengerForm(forms.Form):
    GENDER_CHOICES = (
        ("M", "Male"), 
        ("F", "Female"), 
        ("O", "Other"),
    )

    name = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'placeholder' :"Full Name",  'required': True}), label = "Full Name")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget = forms.Select(attrs={'placeholder' :"Gender",  'required': True}), label = "Gender")
    age = forms.IntegerField(min_value=16, max_value=200, widget = forms.NumberInput(attrs={'placeholder' :"Age",  'required': True}), label = "Age")



class TicketForm(forms.Form):

    def __init__(self, *args, **kwargs):
        COACH_TYPE = (
            ("SL", "SL"), 
            ("AC", "AC"),
        )
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['coachType'] = forms.ChoiceField(choices=COACH_TYPE, widget = forms.Select(attrs={'placeholder' :"Coach Type",  'required': True,}), label = "Coach Type")





class BasePassengerFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                age = form.cleaned_data['age']
                gender = form.cleaned_data['gender']

                # Check that all links have both an anchor and URL
                if not name or not age or not gender:
                    raise forms.ValidationError(
                        'Fill in the data of all passengers',
                        code='missing_data'
                    )




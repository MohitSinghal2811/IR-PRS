from django import forms
from .validators import isTrainNumberUnique, isCreditCardNumberUnique, isEmailUnique, isUserNameUnique



class TrainForm(forms.Form):
    trainNumber = forms.IntegerField(help_text= "Train number should be of 4-5 characters and should be unique", widget = forms.NumberInput(), max_value=99999, min_value=1000, validators = [isTrainNumberUnique, ], label = 'Train Number')
    starts = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={'placeholder' :"Start Station",  'required': True , 'autofocus' : True}), label = 'Source')
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


    

    
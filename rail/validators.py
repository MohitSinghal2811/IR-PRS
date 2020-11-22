from django import forms
from .models import Train, BookingAgent
from django.contrib.auth.models import User
import datetime


def isTrainNumberUnique(value):
    q = Train.objects.filter(trainNumber = value)
    if(q.count() == 1):
        raise forms.ValidationError("Train Number is not unique")

def isUserNameUnique(value):
    q = User.objects.filter(username = value)
    if(q.count() == 1):
        raise forms.ValidationError("User Name already Exists")

def isEmailUnique(value):
    q = BookingAgent.objects.filter(email = value)
    if(q.count() == 1):
        raise forms.ValidationError("Email Address already taken")

def isCreditCardNumberUnique(value):
    q = BookingAgent.objects.filter(creditCardNo = value)
    if(q.count() == 1):
        raise forms.ValidationError("Credit Card Number already taken")

def isDepartureDateValid(value):
    today = datetime.date.today()
    delta = value - today
    if not(delta.days <= 180 and delta.days >= 60):
        raise forms.ValidationError("Departure Date doesn't satisfy the below mentioned constraints")

def trainExists(value):
    q = Train.objects.filter(trainNumber = value)
    if(q.count() == 0):
        raise forms.ValidationError("Train Number not found")
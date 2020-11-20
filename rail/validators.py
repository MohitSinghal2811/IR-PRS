from django import forms
from .models import Train

def isTrainNumberUnique(value):
    q = Train.objects.filter(trainNumber = value)
    if(q.count() == 1):
        raise forms.ValidationError("Train Number is not unique")


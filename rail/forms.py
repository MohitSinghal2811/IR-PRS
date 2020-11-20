from django import forms
from .validators import isTrainNumberUnique


class TrainForm(forms.Form):
    trainNumber = forms.IntegerField(help_text= "Train number should be of 4-5 characters and should be unique", widget = forms.NumberInput(), max_value=99999, min_value=1000, validators = [isTrainNumberUnique, ], label = 'Train Number')
    starts = forms.CharField(max_length = 20, widget = forms.TextInput(), label = 'Source')
    ends = forms.CharField(max_length = 20, widget = forms.TextInput(), label = 'Destination')
    name = forms.CharField(max_length = 30, widget = forms.TextInput(), label = 'Name of the Train')


    def clean(self):
        super(TrainForm, self).clean()
        starts = self.cleaned_data.get('starts')
        ends = self.cleaned_data.get('ends')
        if(starts == ends):
            raise forms.ValidationError('Source and Destination must be different')


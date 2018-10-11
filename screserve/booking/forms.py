from django import forms
from django.forms.widgets import DateTimeInput
from .models import Reservation
from .choices import *

class ReservationForm(forms.ModelForm):
    dateofreservation = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices=field.choices[1:]
        self.fields['officer'].empty_label = None
        self.fields['typeofreservation'].required = False
        self.fields['dateofreservation'].required = False

    class Meta:
        model = Reservation
        fields = ('dateofreservation', 'client', 'turn', 'officer', 'noofguest', 'dateofactualvisit','timeofarrival', 'timeofdeparture', 'typeofreservation', 'cottagenumber','modeofbooking', 'remarks')

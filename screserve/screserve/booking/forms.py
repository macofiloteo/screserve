from django import forms
from .models import Reservation
from django.contrib.auth.models import User
from .choices import *

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices=field.choices[1:]
        self.fields['officer'].empty_label = None
        self.fields['typeofreservation'].required = False

    class Meta:
        model = Reservation
        fields = ('client', 'turn', 'officer', 'noofguest', 'dateofactualvisit','timeofarrival', 'timeofdeparture', 'typeofreservation', 'cottagenumber','modeofbooking', 'remarks')

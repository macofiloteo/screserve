from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from people.models import Profile
from .choices import *
from simple_history.models import HistoricalRecords
# Create your models here.


class Reservation(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client')
    dateofreservation = models.DateTimeField(default=timezone.now)
    referencenumber = models.CharField(max_length=5, default="UNREF")
    noofguest = models.IntegerField()
    dateofactualvisit = models.DateField()
    timeofarrival = models.TimeField()
    timeofdeparture = models.TimeField()
    cottagenumber = models.IntegerField()
    modeofbooking = models.CharField(max_length=3, choices=MODE_OF_BOOKING)
    typeofreservation = models.CharField(max_length=1, choices=TYPES_OF_RESERVATION, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    remarks = models.TextField()
    officer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='officer')
    isdeleted = models.BooleanField(default=False)
    history = HistoricalRecords()
    turn = models.PositiveSmallIntegerField(default=0, blank=True)
    def __str__(self):
        return str(self.dateofreservation)

class MaxNumberOfGuestSettings(models.Model):
    maxnumberofguest = models.IntegerField(default=400)
    def save(self, *args, **kwargs):
        if MaxNumberOfGuestSettings.objects.exists() and not self.pk:
            raise ValidationError('There can be only one MaxNumberOfGuestSettings instance')
        return super(MaxNumberOfGuestSettings, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.maxnumberofguest)

@receiver(post_save, sender=Reservation)
def reservationlog_handler(sender, instance, **kwargs):
    print("It Worked!")

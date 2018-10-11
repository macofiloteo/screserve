from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.conf import settings
from people.storage import OverwriteStorage
import os

from .choices import *

def upload_to(instance, filename):
	pk = instance.pk
	return (os.path.join(str(pk), filename))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(null=True,blank=True, upload_to=upload_to, storage=OverwriteStorage())
    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    address = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    isblocked = models.BooleanField(default=False)
    isdeleted = models.BooleanField(default=False)
    dateregistered = models.DateField(default=timezone.now)
    history = HistoricalRecords()

    def __str__(self):
        return "{}, {} {}.".format(self.lname, self.fname, self.mname[0])

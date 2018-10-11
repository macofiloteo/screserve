from django.contrib import admin
from .models import Reservation, MaxNumberOfGuestSettings
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Reservation, SimpleHistoryAdmin)
admin.site.register(MaxNumberOfGuestSettings)

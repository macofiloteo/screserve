from django.contrib import admin
from .models import Profile
from simple_history.admin import SimpleHistoryAdmin
admin.site.register(Profile, SimpleHistoryAdmin)

import datetime
from django.shortcuts import render
from people.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.shortcuts import redirect
from screserve.booking.models import Reservation, MaxNumberOfGuestSettings
from django.db.models import Sum
from people.views import admin_check

def index(request):
    bookings = Reservation.objects.filter(status='A').values('dateofactualvisit').annotate(sum=Sum('noofguest'))
    maxvisitors = MaxNumberOfGuestSettings.objects.get(pk=1)
    return render(request, 'screserve/index.html', {'events':bookings,'maxvisitor':maxvisitors})

def configure_max_guest(request):
    if request.method == 'POST' and admin_check(request.user):
        booking = MaxNumberOfGuestSettings.objects.get(pk=1)
        booking.maxnumberofguest = request.POST.get("maxvisitor")
        booking.save()
    return redirect('index')

def custom_login(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return login(request)

def custom_logout(request, **kwargs):
    if request.user.is_authenticated:
        return logout(request)
    else:
        return redirect('login')

def print_accepted_reservation(request):
    
    if request.is_ajax():
        reserveddate = request.GET.get("reserveddate")
        reserveddate = datetime.datetime.strptime(reserveddate, "%Y-%m-%d").date()
        
        bookings = Reservation.objects.filter(isdeleted=False, status='A', dateofactualvisit__gte=reserveddate, dateofactualvisit__lte=reserveddate).order_by("typeofreservation", "turn")
        context = {
            'bookings':bookings,
            'reserveddate':reserveddate,
        }
        return render(request, 'screserve/_print_accepted_reservation.html', {'context' : context})

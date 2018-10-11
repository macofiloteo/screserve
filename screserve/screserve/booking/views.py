import datetime
from django.shortcuts import render, get_object_or_404, redirect
from people.models import Profile
from django.http import JsonResponse, HttpResponseServerError
from django.core import serializers
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from people.views import admin_check
from .forms import ReservationForm
from .models import Reservation, MaxNumberOfGuestSettings
from .helpers import RegularOrExcursion

def list_bookings(request):
    datefrom = "0001-01-30"
    dateto = "9999-01-30"
    type = ('R', 'E')

    if 'datefrom' in request.GET and request.GET['datefrom'] != '':
        datefrom = request.GET['datefrom']
    if 'dateto' in request.GET and request.GET['dateto'] != '':
        dateto = request.GET['dateto']
    if 'type' in request.GET and request.GET['type'] != '':
        type = request.GET['type']

    datefrom = datetime.datetime.strptime(datefrom, "%Y-%m-%d").date()
    dateto = datetime.datetime.strptime(dateto, "%Y-%m-%d").date()

    accepted = Reservation.objects.filter(isdeleted=False, status='A', dateofactualvisit__gte=datefrom, dateofactualvisit__lte=dateto, typeofreservation__in=type)
    pending = Reservation.objects.filter(isdeleted=False, status='P', dateofactualvisit__gte=datefrom, dateofactualvisit__lte=dateto, typeofreservation__in=type)
    cancelled = Reservation.objects.filter(isdeleted=False, status='C', dateofactualvisit__gte=datefrom, dateofactualvisit__lte=dateto, typeofreservation__in=type)
    declined = Reservation.objects.filter(isdeleted=False, status='D', dateofactualvisit__gte=datefrom, dateofactualvisit__lte=dateto, typeofreservation__in=type)
    all_bookings = Reservation.objects.filter(isdeleted=False, dateofactualvisit__gte=datefrom, dateofactualvisit__lte=dateto, typeofreservation__in=type)

    context = {
    'accepted':accepted,
    'pending':pending,
    'cancelled':cancelled,
    'declined':declined,
    'all_bookings': all_bookings,
    }
    if request.is_ajax():
        return render(request, 'booking/_list_bookings.html', {'partial_context':context})
    return render(request, 'booking/reservation.html', {'context':context})

def print_booking_details(request):
     if request.is_ajax():
        booking = get_object_or_404(Reservation, pk = request.GET.get("booking_pk"))
        return render(request, 'booking/_print_booking_details.html', {'booking' : booking})

def create_booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            if RegularOrExcursion(form.instance.timeofarrival):
                form.instance.typeofreservation = "E"
            else:
                form.instance.typeofreservation = "R"
            form.save()
            return redirect('list_bookings')
    else:
        form = ReservationForm()
    profiles = Profile.objects.filter(isblocked=False, isdeleted=False)
    officers = Profile.objects.filter(user__is_active=True)
    return render(request, 'booking/createreservation.html', {'form': form, 'profiles':profiles, 'officers':officers,})

def update_booking(request, pk):
    booking_query = get_object_or_404(Reservation, pk=pk)
    if (booking_query.status != 'P' and not admin_check(request.user)):
        return redirect("list_bookings")
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=booking_query)
        if form.is_valid():
            form.save()
            return redirect('list_bookings')
        else:
            return HttpResponseServerError()
    else:
        booking = Reservation.objects.get(pk=pk)
        history = booking.history.all().order_by('-dateofactualvisit')
        group_date = {}
        for hist in history:
            date = hist.history_date.date().strftime('%B %d, %Y')
            if date in group_date:
                group_date[date].append(hist)
            else:
                group_date[date] = []
                group_date[date].append(hist)
        #print(group_date)
        form = ReservationForm()
        return render(request, 'booking/updatereservation.html', {'booking':booking, 'form':form, 'history':history, 'group_date': group_date})

def update_booking_status(request):
    if request.method == 'POST':
        if request.is_ajax():
            issave = True
            bookToBeUpdated = get_object_or_404(Reservation, pk=request.POST.get("booking_pk"))
            if (request.POST.get("booking_status")=='A'):
                if(bookToBeUpdated.turn == 0):
                    reservation_in_a_day = Reservation.objects.filter(isdeleted = False, dateofactualvisit = bookToBeUpdated.dateofactualvisit, typeofreservation = booking_query.typeofreservation)
                    count_queuenumber = reservation_in_a_day.exclude(turn = 0).count()
                    bookToBeUpdated.turn = count_queuenumber + 1
                if (admin_check(request.user)):
                    pass
                else:
                    total_guest = reservation_in_a_day.filter(status = 'A').aggregate(Sum("noofguest"))
                    if(total_guest['noofguest__sum'] == None):
                        total_guest['noofguest__sum'] = 0

                    if (total_guest['noofguest__sum'] + bookToBeUpdated.noofguest > MaxNumberOfGuestSettings.objects.get(pk=1).maxnumberofguest):
                            issave = False
            if (issave):
                bookToBeUpdated.status = request.POST.get("booking_status")
                bookToBeUpdated.save()
                return redirect('list_bookings')
            else:
                return HttpResponseServerError()
    else:
        return HttpResponseServerError()

def get_profile_info_json(request, pk):
    profile = get_object_or_404(Profile, pk = pk)
    json_data = {"birthday":profile.birthday, "sex": profile.sex, "address": profile.address, "contact":profile.contact}
    return JsonResponse({'json_data': json_data})

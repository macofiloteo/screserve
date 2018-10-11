from .models import Reservation
from .models import MaxNumberOfGuestSettings

def num_of_reservation(request):
    reservation_count = Reservation.objects.filter(isdeleted=False).count()
    return {
        'reservation_count': reservation_count,
    }

def max_number_of_guest(request):
    max_guest = MaxNumberOfGuestSettings.objects.get(pk=1)
    return {
        'max_guest': max_guest.maxnumberofguest,
    }
from .models import Profile

def num_of_profile_and_officer(request):
    num_of_clients = Profile.objects.filter(user__isnull=True, isdeleted=False).count()
    num_of_officer = Profile.objects.filter(user__is_active = True).count()
    return {
        'client_count': num_of_clients,
        'officer_count': num_of_officer,
    }

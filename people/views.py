from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.contrib.auth.decorators import user_passes_test
from people.models import Profile
from .forms import ProfileForm, OfficerForm

def admin_check(user):
    for group in user.groups.all():
        if group.name == 'Administrator':
            return True
    return False

def officer_check(user):
    if user == None:
        return False
    for group in user.groups.all():
        if group.name == 'Administrator' or group.name == 'Staff':
            return True
    return False

def list_clients(request):
    clients = Profile.objects.filter(user = None, isdeleted=False)
    return render(request, 'people/client.html', {
        'clients': clients,
    },)

def create_profile(request):
    if (request.method == 'POST'):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_client = form.save()
            return redirect('list_clients')
    else:
        form = ProfileForm()
    return render(request, 'people/createclient.html', {'form':form})


def update_client(request, pk):
    profile_query = get_object_or_404(Profile, pk=pk)
    if officer_check(profile_query.user):
        if profile_query.pk == request.user.pk or admin_check(request.user):
            pass #request.user can update
        else:
            return redirect('index')
    if (request.method == 'POST'):
        form = ProfileForm(request.POST, instance=profile_query)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
        else:
            return redirect('index')
    else:
        return render(request, 'people/updateclient.html', {'user': profile_query})


def delete_client(request):
    if request.is_ajax:
        if (request.method == 'POST'):
            user_query = Profile.objects.get(pk=request.POST.get("client_pk"))
            user_query.isdeleted = True
            user_query.save()
            return JsonResponse({'json_data': request.POST.get("client_pk")})


def active_or_block_client(request):
    if request.is_ajax:
        if (request.method == 'POST'):
            user_query = Profile.objects.get(pk=request.POST.get("client_pk"))
            print(request.POST.get("isblocked"))
            if (request.POST.get("isblocked") == "true"):
                user_query.isblocked = False
            elif (request.POST.get("isblocked") == "false"):
                user_query.isblocked = True
            else:
                return HttpResponse(status=500)
            user_query.save()
            return JsonResponse({'pk': request.POST.get("client_pk"), 'isblocked': user_query.isblocked})

@user_passes_test(admin_check)
def list_officers(request):
    officers = Profile.objects.filter(user__is_active=True)
    return render(request, 'people/officer.html', {'officers':officers,})

@user_passes_test(admin_check)
def create_officer(request):
    if (request.method == 'POST'):
        officer_form = OfficerForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if officer_form.is_valid():
            if profile_form.is_valid():
                user = User.objects.create_user(username=officer_form.cleaned_data['username'], password=officer_form.cleaned_data['password'],)
                position = Group.objects.get(name=officer_form.cleaned_data['groups'])
                position.user_set.add(user)
                new_profile = profile_form.save()
                new_profile.user = user
                new_profile.save()
                return redirect('list_officers')
    else:
        officer_form = OfficerForm()
        profile_form = ProfileForm()
    groups = Group.objects.all()
    return render(request, 'people/createofficer.html', {'groups': groups, 'officer_form':officer_form, 'profile_form': profile_form})

@user_passes_test(admin_check)
def update_officer(request, pk):
    profile = Profile.objects.get(pk=pk)
    role = profile.user.groups.values_list('name',flat=True)
    profile_form = ProfileForm()
    if (request.method == 'POST'):
        officer_form = OfficerForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid() and officer_form.is_valid():
            profile_form.save()
            user = officer_form.save(commit=False)
            user.username = officer_form.cleaned_data['username']
            user.set_password(officer_form.cleaned_data['password'])
            user.groups.clear()
            user.save()
            role = Group.objects.get(name=officer_form.cleaned_data['groups'])
            role.user_set.add(user)
            return redirect('list_officers')
    else:
        officer_form = OfficerForm()
        profile_form = ProfileForm()
    groups = Group.objects.all()
    return render(request, 'people/updateofficer.html', {'officer':profile, 'groups': groups, 'role':role, 'profile_form':profile_form, 'officer_form':officer_form})

@user_passes_test(admin_check)
def delete_officer(request):
    if request.is_ajax:
        if (request.method == 'POST'):
            officer_query = Profile.objects.get(pk=request.POST.get("officer_pk"))
            officer_query.user.is_active = False
            officer_query.user.save()
            return JsonResponse({'json_data': request.POST.get("officer_pk")})

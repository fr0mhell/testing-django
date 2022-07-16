from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Running
from .forms import CreateProfileForm


@login_required
def create_profile(request):
    form = CreateProfileForm(request.POST or None)

    if request.method != 'POST' or not form.is_valid():
        return render(request, 'create_profile.html', {'form': form})

    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    return redirect('trainings:my-trainings')


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (profile := request.user.profile):
        return redirect('trainings:create-profile')

    trainings = Running.objects.all()
    return render(request, 'index.html', context={'trainings': trainings, 'show_all': True})


def my_trainings(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (profile := request.user.profile):
        return redirect('trainings:create-profile')

    trainings = Running.objects.filter(profile=profile)
    return render(request, 'index.html', context={'trainings': trainings, 'show_all': False})

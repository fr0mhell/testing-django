from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from .models import Training, Profile
from .forms import ProfileForm, TrainingForm, ProfileForm2


@login_required
def create_profile(request):

    form = ProfileForm(
        data=request.POST or None,
    )

    if request.method != 'POST' or not form.is_valid():
        context = {'form': form, 'is_edit': False}
        template = 'create_profile.html'
        return render(request, template, context)

    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    return redirect('trainings:my-trainings')


@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if profile.user_id != request.user.id:
        return HttpResponseNotFound('Profile not found')

    form = ProfileForm(
        data=request.POST or None,
        instance=profile,
    )

    if form.is_valid():
        form.save()
        return redirect('trainings:my-trainings')

    context = {
        'form': form,
        'profile_id': profile.id,
        'is_edit': True,
    }
    template = 'create_profile.html'
    return render(request, template, context)


def _show_training_table(request, show_all):
    """Not a view function!"""
    if not request.user.is_authenticated:
        return redirect('login')
    profile_qs = Profile.objects.filter(user=request.user)

    if not profile_qs.exists():
        return redirect('trainings:create-profile')

    trainings = Training.objects.all().select_related(
        'profile',
        'profile__user',
        'training_type',
    )
    profile = profile_qs.first()
    if not show_all:
        trainings = trainings.filter(profile=profile)
    return render(request, 'index.html', context={'trainings': trainings[:100], 'show_all': show_all})


def index(request):
    return _show_training_table(request, show_all=True)


def my_trainings(request):
    return _show_training_table(request, show_all=False)


@login_required
def add_training(request):
    if not (profile := request.user.profile):
        return redirect('trainings:create-profile')

    form = TrainingForm(request.POST or None)

    if request.method != 'POST' or not form.is_valid():
        context = {'form': form, 'is_edit': False}
        template = 'create_training.html'
        return render(request, template, context)

    training = Training(
        started_at=form.cleaned_data['started_at'],
        finished_at=form.cleaned_data['finished_at'],
        training_type=form.cleaned_data['training_type'],
        training_units=form.cleaned_data['training_units'],
        profile=profile,
    )

    # training = form.save(commit=False)
    # training.profile = profile
    training.save()
    return redirect('trainings:my-trainings')


@login_required
def edit_training(request, training_id):
    if not request.user.profile:
        return redirect('trainings:create-profile')

    training = get_object_or_404(Training, id=training_id)

    if training.profile.user_id != request.user.id:
        return HttpResponseNotFound('Training not found')

    form = TrainingForm(request.POST or None, instance=training)

    if form.is_valid():
        form.save()
        return redirect('trainings:my-trainings')

    context = {
        'form': form,
        'training_id': training.id,
        'is_edit': True,
    }
    template = 'create_training.html'
    return render(request, template, context)

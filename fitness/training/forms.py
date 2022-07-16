from django.forms import ModelForm
from .models import Profile, Running


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['weight_kg']


class RunningForm(ModelForm):

    class Meta:
        model = Running
        fields = [
            'action',
            'started_at',
            'finished_at',
        ]

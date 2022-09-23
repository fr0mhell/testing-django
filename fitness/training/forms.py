from django.forms import ModelForm
from .models import Profile, Training


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'weight_kg',
            'height_m',
        ]


class TrainingForm(ModelForm):

    class Meta:
        model = Training
        fields = [
            'training_type',
            'training_units',
            'started_at',
            'finished_at',
        ]

    def full_clean(self):
        return super().full_clean()

    def save(self, commit=True):
        return super().save(commit=commit)

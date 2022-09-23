from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields, ModelChoiceField
from .models import Profile, Training, User


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'weight_kg',
            'height_m',
        ]


class ProfileForm2(ProfileForm):

    user = ModelChoiceField(
        queryset=User.objects.all()
    )


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

    def clean(self):
        clean_data = super().clean()

        started_at = clean_data['started_at']
        finished_at = clean_data['finished_at']

        if started_at >= finished_at:
            raise ValidationError('Start date cannot be later that finish date')

        return clean_data

    # def clean_training_units(self):
    #     if self.cleaned_data['training_units'] < 100:
    #         raise ValidationError('Too small amount!')
    #     return self.cleaned_data['training_units']

    def save(self, commit=True):
        return super().save(commit=commit)

from django.forms import ModelForm
from .models import Profile


class CreateProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['weight_kg']

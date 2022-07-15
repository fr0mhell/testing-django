from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Running)
class RunningAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'duration_hours',
        'distance_km',
        'mean_speed',
        'calories_spent',
    )

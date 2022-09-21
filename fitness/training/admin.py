from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'training_type',
        'finished_at',
        'started_at',
        'duration_hours',
        'distance_km',
        'mean_speed',
        'calories_spent',
    )

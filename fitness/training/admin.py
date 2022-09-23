from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'weight_kg',
        'height_m',
        'running_count',
        'push_ups_count',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_training_types_count()


@admin.register(models.TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'label',
        'action_name',
        'training_count',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_training_count()


@admin.register(models.Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'training_type',
        'finished_at',
        'started_at',
        'duration',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_duration()

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

M_IN_KM: int = 1_000
MIN_IN_H: int = 60
SEC_IN_HOUR = 3_600


class ProfileQuerySet(models.QuerySet):
    ...


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    weight_kg = models.FloatField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name=_('Weight (kilos)'),
    )

    height_m = models.FloatField(
        validators=[
            MinValueValidator(0.1),
        ],
        verbose_name=_('Height (meters)'),
    )

    objects = ProfileQuerySet.as_manager()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'


class TrainingTypeQuerySet(models.QuerySet):
    ...


class TrainingType(models.Model):

    label = models.CharField(
        max_length=255,
        verbose_name=_('Training label'),
    )
    slug = models.SlugField(
        verbose_name=_('Training slug'),
        primary_key=True,
        unique=True,
    )
    action_name = models.CharField(
        max_length=255,
        verbose_name=_('Action name'),
        help_text=_('Training action name (step, repeat, etc.)'),
    )

    objects = TrainingTypeQuerySet.as_manager()

    def __str__(self):
        return self.label

    class Meta:
        ordering = [
            'slug',
        ]


class TrainingQuerySet(models.QuerySet):
    ...


class Training(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='trainings',
    )

    training_type = models.ForeignKey(
        TrainingType,
        on_delete=models.CASCADE,
        related_name='trainings',
    )

    training_units = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        verbose_name=_('Training units'),
        help_text=_('How many training units (steps, repeats, etc.) done during training'),
    )
    started_at = models.DateTimeField(
        verbose_name=_('Started At'),
    )
    finished_at = models.DateTimeField(
        verbose_name=_('Finished At'),
    )

    objects = TrainingQuerySet.as_manager()

    @property
    def duration_hours(self) -> float:
        return (self.finished_at - self.started_at).seconds / SEC_IN_HOUR

    @property
    def distance_km(self) -> float:
        """Dummy implementation to always have value."""
        return 14.5

    @property
    def mean_speed(self) -> float:
        return self.distance_km / self.duration_hours

    @property
    def calories_spent(self) -> float:
        """Dummy implementation to always have value."""
        return 250.0

    def __str__(self):
        return f'{self.training_type}: {self.training_units} {self.training_type.action_name}(s)'

    class Meta:
        ordering = [
            '-finished_at',
            '-started_at',
        ]

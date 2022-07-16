from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

M_IN_KM: int = 1000
MIN_IN_H: int = 60


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

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'


class Training(models.Model):
    LEN_STEP_METERS: float

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    action = models.IntegerField(
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

    @property
    def duration_hours(self) -> float:
        return (self.finished_at - self.started_at).seconds / 3_600

    @property
    def distance_km(self) -> float:
        return self.action * self.LEN_STEP_METERS / M_IN_KM

    @property
    def mean_speed(self) -> float:
        return self.distance_km / self.duration_hours

    @property
    def calories_spent(self) -> float:
        raise NotImplementedError

    def __str__(self):
        return f'{self.__class__.__name__}'

    class Meta:
        abstract = True
        ordering = [
            '-finished_at',
            '-started_at',
        ]


class Running(Training):
    ...
    LEN_STEP_METERS: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 20

    @property
    def calories_spent(self) -> float:
        calories: float = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.mean_speed
            - self.CALORIES_MEAN_SPEED_SHIFT
        )

        cal_per_minute: float = (
            calories
            * self.profile.weight_kg
            / M_IN_KM
        )
        return cal_per_minute * self.duration_hours * MIN_IN_H

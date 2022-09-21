import random
import datetime as dt

from django.core.management.base import BaseCommand

from ...models import Profile, Running
from django.contrib.auth.models import User
from django.utils import timezone as tz

USERS = 20
USER_TRAININGS = [20, 40, 60, 80, 100]


class Command(BaseCommand):
    """Custom `filldb` command.

    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        for i in range(USERS):
            user = User(username=f'user_{i + 1}', email=f'user_{i + 1}@test.test')
            user.set_password(f'user_{i + 1}')
            user.save()

        Profile.objects.bulk_create([
            Profile(
                user=user,
                weight_kg=random.uniform(60, 100),
            ) for user in User.objects.exclude(username='root')
        ])

        for i, profile in enumerate(Profile.objects.exclude(user__username='root')):
            training_num = USER_TRAININGS[i]
            first_training_day = tz.now() - dt.timedelta(days=training_num)

            runnings = []
            for j in range(training_num):
                started_at = first_training_day + dt.timedelta(days=j)
                finished_at = started_at + dt.timedelta(minutes=random.randint(10, 200))
                new_running = Running(
                    profile=profile,
                    action=random.randint(100, 20_000),
                    started_at=started_at,
                    finished_at=finished_at,
                )
                runnings.append(new_running)

            Running.objects.bulk_create(runnings)


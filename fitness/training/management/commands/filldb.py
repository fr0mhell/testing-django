import datetime as dt
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ... import models, constants


User = get_user_model()

DAYS = 180
USERS = 50


class Command(BaseCommand):
    """Custom `filldb` command.

    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        print('Creating Users...')
        for i in range(USERS):
            user = User(username=f'user_{i + 1}', email=f'user_{i + 1}@test.test')
            user.set_password(f'user_{i + 1}')
            user.save()

        print(f'{USERS} Users created')
        print('Creating Profiles...')

        # Create Profile per user
        models.Profile.objects.bulk_create([
            models.Profile(
                user=user,
                weight_kg=random.uniform(60, 120),
                height_m=random.uniform(1.4, 2.1),
            ) for user in User.objects.exclude(username='root')
        ])

        print(f'{USERS} Profiles created')

        profiles = list(models.Profile.objects.all())
        training_types = models.TrainingType.objects.all()
        today = dt.date.today()

        # Create trainings for every of last `DAYS` days
        for i in range(DAYS):
            start_date = today - dt.timedelta(days=i)

            print(f'Creating Trainings for {start_date}...')

            # Every day at least one user has training
            have_training = random.sample(profiles, random.randint(1, USERS))

            tranings = []

            for profile in have_training:
                training_type = random.choice(training_types)
                # Every training starts at 06:00 - 20:00
                started_at = dt.datetime.combine(start_date, dt.time(hour=random.randint(6, 20)))

                # Running lasts 30 - 120 minutes
                if training_type.label == constants.TrainingTypes.RUNNING:
                    finished_at = started_at + dt.timedelta(minutes=random.randint(30, 120))
                    training_units = random.randint(5_000, 15_000)
                # Push up training lasts 15 - 30 minutes
                if training_type.label == constants.TrainingTypes.PUSH_UPS:
                    finished_at = started_at + dt.timedelta(minutes=random.randint(15, 30))
                    training_units = random.randint(20, 300)

                tranings.append(
                    models.Training(
                        profile=profile,
                        training_type=training_type,
                        training_units=training_units,
                        started_at=started_at,
                        finished_at=finished_at,
                    )
                )

            models.Training.objects.bulk_create(tranings)
            print(f'{len(tranings)} Trainings created for {start_date}')

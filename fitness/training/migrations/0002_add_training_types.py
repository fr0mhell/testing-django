from django.db import migrations
from django.utils.text import slugify
from ..constants import TrainingTypes


def add_training_types(apps, schema_editor):
    TrainingType = apps.get_model('training', 'TrainingType')

    running = TrainingType(
        label=TrainingTypes.RUNNING,
        slug=slugify(TrainingTypes.RUNNING),
        action_name='step',
    )
    running.save()

    push_ups = TrainingType(
        label=TrainingTypes.PUSH_UPS,
        slug=slugify(TrainingTypes.PUSH_UPS),
        action_name='repetition',
    )
    push_ups.save()


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_training_types),
    ]

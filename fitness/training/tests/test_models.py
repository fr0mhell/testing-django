from django.test import TestCase
import datetime as dt

from ..models import Running, Profile, M_IN_KM
from django.contrib.auth.models import User


class RunningModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # используем вместо setUpClass
        cls.user_1 = User.objects.create_user(
            username='user_1',
            email='user_1@test.test',
        )
        cls.profile_1 = Profile.objects.create(user=cls.user_1, weight_kg=75.55)
        cls.training_1 = Running.objects.create(
            profile=cls.profile_1,
            action=1_000,
            started_at=dt.datetime(2022, 1, 1, 0, 0),
            finished_at=dt.datetime(2022, 1, 1, 1, 30),
        )
        cls.duration_hours = 1.5
        cls.distance_km = cls.training_1.action * cls.training_1.LEN_STEP_METERS / M_IN_KM
        cls.mean_speed = cls.distance_km / cls.duration_hours

    def test_training_properties(self):
        test_data = [
            ['duration_hours', self.duration_hours],
            ['distance_km', self.distance_km],
            ['mean_speed', self.mean_speed],
        ]

        for prop_name, expected_value in test_data:
            with self.subTest(property_name=prop_name, expected_value=expected_value):
                self.assertEqual(
                    getattr(self.training_1, prop_name),
                    expected_value,
                )

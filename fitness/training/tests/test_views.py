from http import HTTPStatus

from django.test import TestCase, Client
import datetime as dt
from django.shortcuts import reverse

from ..models import Running, Profile
from django.contrib.auth.models import User


class IndexViewTestCase(TestCase):

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

        cls.user_2 = User.objects.create_user(
            username='user_2',
            email='user_2@test.test',
        )
        cls.profile_2 = Profile.objects.create(user=cls.user_2, weight_kg=90)
        cls.training_2 = Running.objects.create(
            profile=cls.profile_2,
            action=1_000,
            started_at=dt.datetime(2022, 2, 1, 0, 0),
            finished_at=dt.datetime(2022, 2, 1, 1, 30),
        )

        cls.anon_client = Client()
        cls.client_1 = Client()
        cls.client_1.force_login(cls.user_1)
        cls.client_2 = Client()
        cls.client_2.force_login(cls.user_2)

        cls.urls_to_test = [
            [reverse('trainings:index'), 'index.html'],
            [reverse('trainings:my-trainings'), 'index.html'],
        ]

    def test_unauth_redirects_to_login(self):
        login_url = reverse('login')

        for url, _ in self.urls_to_test:
            with self.subTest(url=url):
                response = self.anon_client.get(url)
                self.assertRedirects(response, login_url)

    def test_auth_no_profile_redirects_to_create_profile(self):
        create_profile = reverse('trainings:create-profile')
        self.profile_1.delete()

        for url, _ in self.urls_to_test:
            with self.subTest(url=url):
                response = self.client_1.get(url)
                self.assertRedirects(response, create_profile)

    def test_index_shows_all_trainings(self):
        index_url, template = self.urls_to_test[0]
        response = self.client_1.get(index_url)
        self.assertTemplateUsed(response, template)

        received_trainings = response.context['trainings']
        self.assertEqual(
            Running.objects.count(),
            len(received_trainings),
        )

        ids = [t.id for t in received_trainings]
        self.assertIn(self.training_1.id, ids)
        self.assertIn(self.training_2.id, ids)

    def test_my_trainings_shows_only_my_trainings(self):
        my_trainings, template = self.urls_to_test[1]
        response = self.client_1.get(my_trainings)

        received_trainings = response.context['trainings']
        self.assertEqual(
            len(received_trainings),
            1,
        )

        ids = [t.id for t in received_trainings]
        self.assertIn(self.training_1.id, ids)
        self.assertNotIn(self.training_2.id, ids)

    def test_new_training_on_index(self):
        index_url, template = self.urls_to_test[0]
        new_training = Running.objects.create(
            profile=self.profile_2,
            action=1_000,
            started_at=dt.datetime(2022, 2, 1, 0, 0),
            finished_at=dt.datetime(2022, 2, 1, 1, 30),
        )

        response = self.client_2.get(index_url)

        received_trainings = response.context['trainings']
        self.assertEqual(
            Running.objects.count(),
            len(received_trainings),
        )
        ids = [t.id for t in received_trainings]
        self.assertIn(new_training.id, ids)

    def test_new_training_on_my_trainings(self):
        my_trainings, template = self.urls_to_test[1]
        new_training = Running.objects.create(
            profile=self.profile_2,
            action=1_000,
            started_at=dt.datetime(2022, 2, 1, 0, 0),
            finished_at=dt.datetime(2022, 2, 1, 1, 30),
        )

        response = self.client_2.get(my_trainings)

        received_trainings = response.context['trainings']
        self.assertEqual(
            Running.objects.filter(profile__user_id=self.profile_2.id).count(),
            len(received_trainings),
        )
        ids = [t.id for t in received_trainings]
        self.assertIn(new_training.id, ids)

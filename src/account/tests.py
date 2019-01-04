from rest_framework import status
from faker import Faker
import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile
from .serializers import ProfileSerializer

fake = Faker()

fake_email = 'fake@fake.com'


class AccountsTests(APITestCase):

    def setUp(self):
        # Users

        User.objects.create(username='admin', is_superuser=True, is_staff=True) \
            .set_password('adminpw')
        User.objects.create(username='mod', is_superuser=False, is_staff=True) \
            .set_password('modpw')
        User.objects.create(username='user', is_superuser=False, is_staff=False) \
            .set_password('userpw')
        User.objects.create(username='other_user', is_superuser=False, is_staff=False) \
            .set_password('userpw')

        # Profiles

        for user in User.objects.all():
            Profile.objects.create(user=user,
                                   about_me=fake.paragraph(nb_sentences=4),
                                   is_score_visible=True,
                                   ranked=True)

    # -------------------------------------------------------------------------
    # LIST view
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    def test_get_list_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        url = reverse('profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.all().count())

        self.client.logout()

    def test_get_list_mod(self):
        self.client.force_login(User.objects.get(username="mod"))
        url = reverse('profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.all().count())

        self.client.logout()

    def test_get_list_user(self):
        self.client.force_login(User.objects.get(username="user"))
        url = reverse('profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_get_list_no_login(self):
        url = reverse('profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------------------------------------------------
    # SINGLE view
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    def test_get_single_random_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        get_idx = Profile.objects.order_by('?').first().pk
        url = ''.join([reverse('profile-list'), str(get_idx), '/'])
        response = self.client.get(url)

        profile = Profile.objects.get(pk=get_idx)
        serializer = ProfileSerializer(profile)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        self.client.logout()

    def test_get_single_random_mod(self):
        self.client.force_login(User.objects.get(username='mod'))
        get_idx = Profile.objects.order_by('?').first().pk
        url = ''.join([reverse('profile-list'), str(get_idx), '/'])
        response = self.client.get(url)

        profile = Profile.objects.get(pk=get_idx)
        serializer = ProfileSerializer(profile)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        self.client.logout()

    def test_get_single_own_user(self):
        self.client.force_login(User.objects.get(username='user'))
        get_idx = User.objects.get(username='user').pk
        url = ''.join([reverse('profile-list'), str(get_idx), '/'])
        response = self.client.get(url)

        profile = Profile.objects.get(pk=get_idx)
        serializer = ProfileSerializer(profile)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        self.client.logout()

    def test_get_single_not_own_user(self):
        self.client.force_login(User.objects.get(username='user'))
        get_idx = User.objects.get(username='other_user').pk
        url = ''.join([reverse('profile-list'), str(get_idx), '/'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_get_single_non_exist_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        get_idx = Profile.objects.all().count() + 1
        url = ''.join([reverse('profile-list'), str(get_idx), '/'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.logout()

    # -------------------------------------------------------------------------
    # PUT
    # -------------------------------------------------------------------------

    def test_put_single_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        put_idx = User.objects.all()[random.randint(0, User.objects.all().count() - 1)].pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": User.objects.get(pk=put_idx).username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": False,
                "is_active": True
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_put_single_mod(self):
        self.client.force_login(User.objects.get(username='mod'))
        put_idx = User.objects.all()[random.randint(0, User.objects.all().count() - 1)].pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": User.objects.get(pk=put_idx).username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": False,
                "is_active": True
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_put_single_user_other(self):
        user = User.objects.get(username='user')
        self.client.force_login(user)

        other_user = User.objects.get(username='other_user')

        put_idx = other_user.pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": other_user.username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": other_user.is_staff,
                "is_active": other_user.is_active
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_put_single_user_own_valid(self):
        user = User.objects.get(username='user')
        self.client.force_login(user)
        put_idx = user.pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": user.username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": user.is_staff,
                "is_active": user.is_active
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_user_change_own_is_active(self):
        user = User.objects.get(username='user')
        self.client.force_login(user)
        put_idx = user.pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": user.username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": user.is_staff,
                "is_active": not user.is_active
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.is_active, User.objects.get(username=user.username).is_active)

        self.client.logout()

    def test_user_change_own_is_staff(self):
        user = User.objects.get(username='user')
        self.client.force_login(user)
        put_idx = user.pk
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        data = {
            "id": put_idx,
            "user": {
                "username": user.username,
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": not user.is_staff,
                "is_active": user.is_active
            },
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.is_staff, User.objects.get(username=user.username).is_staff)

        self.client.logout()


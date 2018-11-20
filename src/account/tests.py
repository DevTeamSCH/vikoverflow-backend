from rest_framework import status
from faker import Faker
import random
from PIL import Image
from tempfile import NamedTemporaryFile

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.client import encode_multipart

from .models import Profile
from .serializers import ProfileSerializer

fake = Faker()

fake_email = 'fake@fake.com'
fake_img = "jankaluza_superabstraction.jpg"


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

        # Accounts

        for i in range(1, User.objects.all().count() + 1):
            Profile.objects.create(user=User.objects.get(pk=i),
                                   avatar=fake_img,
                                   about_me=fake.paragraph(nb_sentences=4),
                                   is_score_visible=1 & i,
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_get_list_no_login(self):
        url = reverse('profile-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------------------------------------------------
    # POST
    # -------------------------------------------------------------------------

    def test_post_list_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        url = reverse('profile-list')
        data = {
            "user": {
                "username": fake.text(max_nb_chars=20),
                "email": fake_email,
                "first_name": fake.text(max_nb_chars=20),
                "last_name": fake.text(max_nb_chars=20),
                "is_staff": bool(random.getrandbits(1)),
                "is_active": bool(random.getrandbits(1))
            },
            "avatar": fake_img,
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": bool(random.getrandbits(1)),
            "ranked": bool(random.getrandbits(1))
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.logout()

    # -------------------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------------------

    def test_delete_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        del_idx = Profile.objects.order_by('?').first().pk
        url = ''.join([reverse('profile-list'), str(del_idx), '/'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.logout()

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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        put_idx = 3
        url = ''.join([reverse('profile-list'), str(put_idx), '/'])

        image = Image.new('RGB', (50, 50))
        tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

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
            "avatar": tmp_file,
            "about_me": fake.text(max_nb_chars=50),
            "is_score_visible": True,
            "ranked": True
        }
        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = self.client.put(url, content, content_type=content_type)
        # response = self.client.put(url, data, content_type='multipart/form-data')

        # print(data)
        # print('-----------')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()






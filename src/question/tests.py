from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from taggit.models import Tag

starting_amount = 5
added_amount = 5


class TagTests(APITestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(username='admin', is_superuser=True, is_staff=True, password='adminpass'),
                User(username='mod', is_staff=True, password='modpass'),
                User(username='csicska', is_staff=False, password='csicskapass')
            ]
        )

        for i in range(1, starting_amount + 1):
            Tag.objects.create(name="Tag"+str(i), slug="tag"+str(i))

    # -------------------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------------------
    def test_get_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        for i in range(1, starting_amount + 1):
            url = "http://127.0.0.1:8000/api/v1/tags/"+str(i)+"/"
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.logout()

    def test_get_mod(self):
        self.client.force_login(User.objects.get(username="mod"))
        for i in range(1, starting_amount + 1):
            url = "http://127.0.0.1:8000/api/v1/tags/"+str(i)+"/"
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.logout()

    def test_get_csicska(self):
        self.client.force_login(User.objects.get(username="csicska"))
        for i in range(1, starting_amount + 1):
            url = "http://127.0.0.1:8000/api/v1/tags/"+str(i)+"/"
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.logout()

    # ----------------------------------------------------------------------------------------
    # PUT
    # ----------------------------------------------------------------------------------------
    def test_put_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        for i in range(starting_amount + 1, starting_amount + 1 + added_amount):
            url = "http://127.0.0.1:8000/api/v1/tags/" + str(i) + "/"
            data = {
                "url": "/api/v1/tags/" + str(i) + "/",
                "name": "Tag" + str(i),
                "slug": "tag" + str(i)
            }
            object_count = Tag.objects.count()
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Tag.objects.count(), object_count + 1)
        self.client.logout()

    def test_put_mod(self):
        self.client.force_login(User.objects.get(username="mod"))
        for i in range(starting_amount + 1, starting_amount + 1 + added_amount):
            url = "http://127.0.0.1:8000/api/v1/tags/" + str(i) + "/"
            data = {
                "url": "/api/v1/tags/" + str(i) + "/",
                "name": "Tag" + str(i),
                "slug": "tag" + str(i)
            }
            object_count = Tag.objects.count()
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Tag.objects.count(), object_count + 1)
        self.client.logout()

    def test_put_csicska(self):
        self.client.force_login(User.objects.get(username="csicska"))
        for i in range(starting_amount + 1, starting_amount + 1 + added_amount):
            url = "http://127.0.0.1:8000/api/v1/tags/" + str(i) + "/"
            data = {
                "url": "/api/v1/tags/" + str(i) + "/",
                "name": "Tag" + str(i),
                "slug": "tag" + str(i)
            }
            response = self.client.put(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_put_existing_name(self):
        self.client.force_login(User.objects.get(username="mod"))
        url = "http://127.0.0.1:8000/api/v1/tags/6/"
        data = {
                "url": "/api/v1/tags/6/",
                "name": "Tag3",
                "slug": "tag6"
            }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_put_existing_slug(self):
        self.client.force_login(User.objects.get(username="mod"))
        url = "http://127.0.0.1:8000/api/v1/tags/6/"
        data = {
                "url": "/api/v1/tags/6/",
                "name": "Tag6",
                "slug": "tag3"
            }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_overwrite_tag(self):
        self.client.force_login(User.objects.get(username="mod"))
        self.assertEqual(Tag.objects.get(pk=1).name, "Tag1")
        url = "http://127.0.0.1:8000/api/v1/tags/1/"
        data = {
                "url": "/api/v1/tags/1/",
                "name": "Tag6",
                "slug": "tag6"
            }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(pk=1).name, "Tag6")

    # ---------------------------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------------------------

    def test_delete_admin(self):
        self.client.force_login(User.objects.get(username='admin'))
        del_idx = 1
        url = "http://127.0.0.1:8000/api/v1/tags/"+str(del_idx)+"/"
        object_count = Tag.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), object_count - 1)
        self.client.logout()

    def test_delete_staff(self):
        self.client.force_login(User.objects.get(username='mod'))
        del_idx = 1
        url = "http://127.0.0.1:8000/api/v1/tags/" + str(del_idx) + "/"
        object_count = Tag.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), object_count - 1)
        self.client.logout()

    def test_delete_csicska(self):
        self.client.force_login(User.objects.get(username='csicska'))
        del_idx = 1
        url = "http://127.0.0.1:8000/api/v1/tags/" + str(del_idx) + "/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

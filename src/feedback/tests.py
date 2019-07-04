from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ticket
from django.urls import reverse
import random
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class TicketListTest(APITestCase):
    def setUp(self):

        # Users
        User.objects.create(username="admin", is_superuser=True, is_staff=True).set_password("adminpass")
        User.objects.create(username="mod", is_staff=True).set_password("modpass")
        User.objects.create(username="csicska").set_password("csicskapass")

        # Tickets
        for i in range(5):
            Ticket.objects.create(
                title=fake.text(max_nb_chars=50),
                text=fake.paragraph(nb_sentences=4),
                kind_of=("BUG" if bool(random.getrandbits(1)) else "FEATURE"),
            )

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    def test_get_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        url = reverse("ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.client.logout()

    def test_get_staff(self):
        self.client.force_login(User.objects.get(username="mod"))
        url = reverse("ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.client.logout()

    def test_get_user(self):
        self.client.force_login(User.objects.get(username="csicska"))
        url = reverse("ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_get_no_login(self):
        url = reverse("ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------------------------------------------------
    # POST
    # -------------------------------------------------------------------------

    def test_post_user(self):
        self.client.force_login(User.objects.get(username="csicska"))
        object_count = Ticket.objects.count()
        url = reverse("ticket-list")
        data = {"title": fake.text(max_nb_chars=50), "text": fake.paragraph(nb_sentences=4), "kind_of": "BUG"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), object_count + 1)
        self.client.logout()

    def test_post_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        object_count = Ticket.objects.count()
        url = reverse("ticket-list")
        data = {"title": fake.text(max_nb_chars=50), "text": fake.paragraph(nb_sentences=4), "kind_of": "FEATURE"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), object_count + 1)
        self.client.logout()

    def test_post_staff(self):
        self.client.force_login(User.objects.get(username="mod"))
        object_count = Ticket.objects.count()
        url = reverse("ticket-list")
        data = {"title": fake.text(max_nb_chars=50), "text": fake.paragraph(nb_sentences=4), "kind_of": "FEATURE"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), object_count + 1)
        self.client.logout()

    def test_post_no_login(self):
        url = reverse("ticket-list")
        data = {"title": fake.text(max_nb_chars=50), "text": fake.paragraph(nb_sentences=4), "kind_of": "BUG"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_admin_nonsense(self):
        self.client.force_login(User.objects.get(username="admin"))
        url = reverse("ticket-list")
        data = {"title": fake.text(max_nb_chars=50), "text": fake.paragraph(nb_sentences=4), "kind_of": "FAKE TYPE"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    # -------------------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------------------

    def test_delete_admin(self):
        self.client.force_login(User.objects.get(username="admin"))
        del_idx = Ticket.objects.order_by("?").first().pk
        url = "".join([reverse("ticket-list"), str(del_idx), "/"])
        object_count = Ticket.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), object_count - 1)
        self.client.logout()

    def test_delete_staff(self):
        self.client.force_login(User.objects.get(username="mod"))
        del_idx = Ticket.objects.order_by("?").first().pk
        url = "".join([reverse("ticket-list"), str(del_idx), "/"])
        object_count = Ticket.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), object_count - 1)
        self.client.logout()

    def test_delete_user(self):
        self.client.force_login(User.objects.get(username="csicska"))
        del_idx = Ticket.objects.order_by("?").first().pk
        url = "".join([reverse("ticket-list"), str(del_idx), "/"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

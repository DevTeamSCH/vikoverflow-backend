from rest_framework.test import APITestCase
from faker import Faker
import random
from .models import Votes, Comment
from django.contrib.auth.models import User
from account.models import Profile
from django.urls import reverse
from rest_framework import status

fake = Faker()
users = ['alma', 'korte', 'citrom']

class CommentTestCase(APITestCase):
    def setUp(self):
        # Accounts
        for u in users:
            # Users
            name = fake.simple_profile()['name'].split(' ')
            User.objects.create(
                username=u,
                first_name=name[0],
                last_name=name[1]
            )
            # Profiles
            Profile.objects.create(
                user=User.objects.get(username=u)
            )
        # Comments
        for j in range(5):
            owner = random.choice(users[1:])
            v = Votes()
            v.save()
            if j in [1,4]:
                v.upvoters.add(Profile.objects.get(user__username=users[0]))
            if j == 2:
                v.downvoters.add(Profile.objects.get(user__username=users[0]))
            Comment.objects.create(
                text=fake.paragraph(nb_sentences=4),
                owner=Profile.objects.get(user__username=owner),
                show_username=bool(random.getrandbits(1)),
                votes=v
            )


    def test_user_vote(self):
        self.client.force_login(User.objects.get(username=users[0]))
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in [1,2,4]:
            self.assertTrue(response.data[i]['user_vote'])
        self.client.logout()

    def test_no_login(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in [1,2,4]:
            self.assertFalse(response.data[i]['user_vote'])

# from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from account.models import Profile
from common.models import Votes
from .models import Question

class VotingTestCase(APITestCase):

    question = None
    upvoters = None
    downvoters = None
    url = None
    voter = None


    def setUp(self):
        # Users
        submitter = Profile.objects.create(
            user=User.objects.create(
                username='submitter'
            )
        )
        voter = Profile.objects.create(
            user=User.objects.create(
                username='voter',
            )
        )
        # Question
        question = Question.objects.create(
            title='What is love?',
            text='Baby don\'t hurt me!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )


    def prepare(self):
        self.question = Question.objects.all()[0]
        pk = self.question.id
        questions_url = 'http://localhost:8000/api/v1/questions/'
        self.upvoters = self.question.votes.upvoters
        self.downvoters = self.question.votes.downvoters
        self.url = ''.join([questions_url, str(pk), '/'])
        self.voter = User.objects.get(username='voter')


class OnePersonVotingTestCase(VotingTestCase):


    def test_zero_votes(self):
        self.prepare()
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)


    def test_up_up(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'up'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)

        response = self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


    def test_up_down(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'up'})
        response = self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)


    def test_down_up(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'down'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)

        response = self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


    def test_down_down(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'down'})
        response = self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


class TwoPeopleVotingTest(VotingTestCase):

    voter2 = None


    def setUp(self):
        super().setUp()
        voter2 = Profile.objects.create(
            user=User.objects.create(
                username='voter2',
            )
        )


    def prepare(self):
        super().prepare()
        self.voter2 = User.objects.get(username='voter2')


    def test_up_up(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 2)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 1)


    def test_up_down(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 1)


    def test_down_up(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 1)


    def test_down_down(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 2)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 1)

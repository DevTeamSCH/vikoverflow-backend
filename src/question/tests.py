from django.contrib.auth.models import User
from taggit.models import Tag
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status


from account.models import Profile
from common.models import Votes
from .models import Question, Answer, Comment

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

class VotingTestCase(APITestCase):
    model = None
    url_name = None

    abstract_comment = None
    upvoters = None
    downvoters = None
    url = None
    voter = None


    def prepare(self):
        self.abstract_comment = self.model.objects.all()[0]
        abstract_comment_url = ''.join(['http://localhost:8000/api/v1/', self.url_name, '/'])
        self.upvoters = self.abstract_comment.votes.upvoters
        self.downvoters = self.abstract_comment.votes.downvoters
        self.url = ''.join([abstract_comment_url, str(self.abstract_comment.id), '/vote/'])
        self.voter = User.objects.get(username='voter')


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
        # Content
        question = Question.objects.create(
            title='What is love?',
            text='Baby don\'t hurt me!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )
        answer = Answer.objects.create(
            text='I like apples.',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter,
            parent=question,
            is_accepted=False
        )
        comment = Comment.objects.create(
            text='Apples suck.',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter,
            parent_answer=answer
        )


class OneVoterQuestion(VotingTestCase):
    model = Question
    url_name = 'questions'


    def test_not_exist(self):
        self.prepare()
        abstract_comment_url = ''.join(['http://localhost:8000/api/v1/', self.url_name, '/'])
        self.url = ''.join([abstract_comment_url, str(100), '/vote/'])
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_permissions(self):
        self.prepare()
        response = self.client.put(self.url, {'user_vote': 'up'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_zero_votes(self):
        self.prepare()
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)


    def test_up(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


    def test_down(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)


    def test_none(self):
        self.prepare()
        self.client.force_login(self.voter)
        response = self.client.put(self.url, {'user_vote': 'none'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


class OneVoterAnswer(OneVoterQuestion):
    model = Answer
    url_name = 'answers'


class OneVoterComment(OneVoterQuestion):
    model = Comment
    url_name = 'comments'


class TwoVotersQuestion(VotingTestCase):
    model = Question
    url_name = 'questions'

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
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 0)


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
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)


    def test_up_none(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'up'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'none'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 1)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 0)


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
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 1)


    def test_down_none(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'down'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'none'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 1)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 0)


    def test_none_none(self):
        self.prepare()
        self.client.force_login(self.voter)
        self.client.put(self.url, {'user_vote': 'none'})
        self.client.logout()
        self.client.force_login(self.voter2)
        self.client.put(self.url, {'user_vote': 'none'})
        self.client.logout()

        self.assertEqual(self.upvoters.all().count(), 0)
        self.assertEqual(self.downvoters.all().count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter).count(), 0)
        self.assertEqual(self.upvoters.filter(user=self.voter2).count(), 0)
        self.assertEqual(self.downvoters.filter(user=self.voter2).count(), 0)


class TwoVotersAnswer(TwoVotersQuestion):
    model = Answer
    url_name = 'answers'


class TwoVotersComment(TwoVotersQuestion):
    model = Comment
    url_name = 'comments'

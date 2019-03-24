from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from account.models import Profile
from common.models import Votes
from .models import Question, Answer, Comment


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
        Profile.objects.create(
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
        Comment.objects.create(
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
        Profile.objects.create(
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


class AnswerQuestionTestCase(APITestCase):
    url = ''

    def setUp(self):
        # Users
        submitter = Profile.objects.create(
            user=User.objects.create(
                username='submitter'
            )
        )
        Profile.objects.create(
            user=User.objects.create(
                username='answerer',
            )
        )
        # Content
        Question.objects.create(
            title='What is love?',
            text='Baby don\'t hurt me!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )

        # Set up URL
        question_pk = Question.objects.filter(title='What is love?')[0].pk
        self.url = reverse("questions-answers", args=[question_pk])

    def test_no_login(self):
        data = {
            "text": "No more",
            "show_username": False
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid(self):
        answerer_user = User.objects.get(username='answerer')
        self.client.force_login(answerer_user)

        data = {
            "text": "No more",
            "show_username": False
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_answer = Answer.objects.filter(owner=Profile.objects.get(user=answerer_user))[0]
        self.assertEqual(new_answer.text, data['text'])
        self.assertEqual(new_answer.show_username, data['show_username'])
        self.assertEqual(new_answer.parent, Question.objects.get(title='What is love?'))

        self.client.logout()

    def test_invalid_data(self):
        answerer_user = User.objects.get(username='answerer')
        self.client.force_login(answerer_user)

        data_without_text = {
            "show_username": False
        }

        response = self.client.post(self.url, data=data_without_text, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data_without_show_username = {
            "text": "No more"
        }

        response = self.client.post(self.url, data=data_without_show_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteQuestionTestCase(APITestCase):
    url = ''

    def setUp(self):
        # Users
        submitter = Profile.objects.create(
            user=User.objects.create(
                username='submitter'
            )
        )
        Profile.objects.create(
            user=User.objects.create(
                username='other_user',
            )
        )
        # Content
        Question.objects.create(
            title='What is love?',
            text='Baby don\'t hurt me!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )

        # Set up URL
        question_pk = Question.objects.filter(title='What is love?')[0].pk
        self.url = reverse("questions-detail", args=[question_pk])

    def test_no_login(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner(self):
        submitter_user = User.objects.get(username='submitter')
        self.client.force_login(submitter_user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.filter(owner__user=submitter_user).count(), 0)

        self.client.logout()

    def test_other_user(self):
        submitter_user = User.objects.get(username='submitter')
        other_user = User.objects.get(username='other_user')
        self.client.force_login(other_user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.filter(owner__user=submitter_user).count(), 1)


class PutQuestionTestCase(APITestCase):
    url = ''

    def setUp(self):
        # Users
        submitter = Profile.objects.create(
            user=User.objects.create(
                username='submitter'
            )
        )
        Profile.objects.create(
            user=User.objects.create(
                username='other_user',
            )
        )
        # Content
        Question.objects.create(
            title='What is love?',
            text='Baby don\'t hurt me!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )

        # Set up URL
        question_pk = Question.objects.filter(title='What is love?')[0].pk
        self.url = reverse("questions-detail", args=[question_pk])

    def test_no_login(self):
        data = {
            "title": "Test title",
            "text": "Test text",
            "tags": [
                "test",
                "put"
            ]
        }

        response = self.client.put(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner(self):
        submitter_user = User.objects.get(username='submitter')
        self.client.force_login(submitter_user)

        data = {
            "title": "Test title",
            "text": "Test text",
            "tags": [
                "test",
                "put"
            ]
        }

        response = self.client.put(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question = Question.objects.get(owner__user=submitter_user)
        self.assertEqual(question.title, data['title'])
        self.assertEqual(question.text, data['text'])
        for tag in question.tags.all():
            self.assertTrue(tag.name in data["tags"])

        self.client.logout()

    def test_other_user(self):
        other_user = User.objects.get(username='other_user')
        self.client.force_login(other_user)

        data = {
            "title": "Test title",
            "text": "Test text",
            "tags": [
                "test",
                "put"
            ]
        }

        response = self.client.put(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()


class EditAnswerTestCase(APITestCase):

    def setUp(self):
        # Users
        submitter = Profile.objects.create(
            user=User.objects.create(
                username='submitter'
            )
        )

        Profile.objects.create(
            user=User.objects.create(
                username='other_user'
            )
        )

        # Content
        question = Question.objects.create(
            title='What does the fox say?',
            text='But there\'s one sound\n'
                 + 'That no one knows\n'
                 + 'What does the fox say?',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter
        )
        Answer.objects.create(
            text='Ring-ding-ding-ding-dingeringeding!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=submitter,
            parent=question,
            is_accepted=False
        )

    def test_edit_text_no_login(self):
        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        data = {
            "text": "Hatee-hatee-hatee-ho!"
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_text_answer_owner(self):
        submitter = User.objects.get(username='submitter')
        self.client.force_login(submitter)

        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        new_text = "Hatee-hatee-hatee-ho!"

        data = {
            "text": new_text
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Answer.objects.get(id=answer_id).text, new_text)

        self.client.logout()

    def test_edit_text_other_user(self):
        other_user = User.objects.get(username='other_user')
        self.client.force_login(other_user)

        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        new_text = "Hatee-hatee-hatee-ho!"

        data = {
            "text": new_text
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()


class AcceptAnswerTestCase(APITestCase):

    def setUp(self):
        # Users
        question_submitter = Profile.objects.create(
            user=User.objects.create(
                username='question_submitter'
            )
        )

        answer_submitter_0 = Profile.objects.create(
            user=User.objects.create(
                username='answer_submitter_0'
            )
        )

        answer_submitter_1 = Profile.objects.create(
            user=User.objects.create(
                username='answer_submitter_1'
            )
        )

        # Content
        question = Question.objects.create(
            title='What does the fox say?',
            text='But there\'s one sound\n'
                 + 'That no one knows\n'
                 + 'What does the fox say?',
            votes=Votes.objects.create(),
            show_username=True,
            owner=question_submitter
        )
        Answer.objects.create(
            text='Ring-ding-ding-ding-dingeringeding!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=answer_submitter_0,
            parent=question,
            is_accepted=True
        )

        Answer.objects.create(
            text='Hatee-hatee-hatee-ho!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=answer_submitter_1,
            parent=question,
            is_accepted=False
        )

    def test_accept_answer_no_login(self):
        answer_id = Answer.objects.get(
            text='Hatee-hatee-hatee-ho!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Answer.objects.get(id=answer_id).is_accepted)

    def test_accept_answer_question_owner(self):
        question_submitter = User.objects.get(username='question_submitter')
        self.client.force_login(question_submitter)

        answer_id = Answer.objects.get(
            text='Hatee-hatee-hatee-ho!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Answer.objects.get(id=answer_id).is_accepted)

        self.client.logout()

    def test_accept_answer_other_user(self):
        other_user = User.objects.get(username='answer_submitter_0')
        self.client.force_login(other_user)

        answer_id = Answer.objects.get(
            text='Hatee-hatee-hatee-ho!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Answer.objects.get(id=answer_id).is_accepted)

        self.client.logout()

    def test_unaccept_answer_no_login(self):
        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": False
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unaccept_answer_question_owner(self):
        question_submitter = User.objects.get(username='question_submitter')
        self.client.force_login(question_submitter)

        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": False
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Answer.objects.get(id=answer_id).is_accepted)

        self.client.logout()

    def test_unaccept_answer_other_user(self):
        other_user = User.objects.get(username='answer_submitter_0')
        self.client.force_login(other_user)

        answer_id = Answer.objects.get(
            text='Ring-ding-ding-ding-dingeringeding!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        data = {
            "accepted": False
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_key_error(self):
        question_submitter = User.objects.get(username='question_submitter')
        self.client.force_login(question_submitter)

        answer_id = Answer.objects.get(
            text='Hatee-hatee-hatee-ho!'
        ).id
        url = reverse('answers-accept', args=[answer_id])

        # Missing "accepted" key in request data
        data = {
            "": True
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Answer.objects.get(id=answer_id).is_accepted)

        self.client.logout()


class DeleteAnswerTestCase(APITestCase):

    def setUp(self):
        # Users
        question_submitter = Profile.objects.create(
            user=User.objects.create(
                username='question_submitter'
            )
        )

        answer_submitter_0 = Profile.objects.create(
            user=User.objects.create(
                username='answer_submitter_0'
            )
        )

        answer_submitter_1 = Profile.objects.create(
            user=User.objects.create(
                username='answer_submitter_1'
            )
        )

        # Content
        question = Question.objects.create(
            title='What does the fox say?',
            text='But there\'s one sound\n'
                 + 'That no one knows\n'
                 + 'What does the fox say?',
            votes=Votes.objects.create(),
            show_username=True,
            owner=question_submitter
        )
        Answer.objects.create(
            text='Ring-ding-ding-ding-dingeringeding!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=answer_submitter_0,
            parent=question,
            is_accepted=True
        )

        Answer.objects.create(
            text='Hatee-hatee-hatee-ho!',
            votes=Votes.objects.create(),
            show_username=True,
            owner=answer_submitter_1,
            parent=question,
            is_accepted=False
        )

    def test_delete_no_login(self):
        answer_id = Answer.objects.get(
            text='Hatee-hatee-hatee-ho!'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_answer(self):
        answer_submitter = User.objects.get(username='answer_submitter_0')
        self.client.force_login(answer_submitter)

        answer_id = Answer.objects.get(
            owner__user=answer_submitter
        ).id
        url = reverse('answers-detail', args=[answer_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()

    def test_delete_other_user(self):
        other_user = User.objects.get(username='answer_submitter_1')
        self.client.force_login(other_user)

        answer_id = Answer.objects.get(
            owner__user__username='answer_submitter_0'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

    def test_delete_question_submitter(self):
        question_submitter = User.objects.get(username='question_submitter')
        self.client.force_login(question_submitter)

        answer_id = Answer.objects.get(
            owner__user__username='answer_submitter_0'
        ).id
        url = reverse('answers-detail', args=[answer_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

from django.test import TestCase
from common.models import Comment, Votes
from question.models import Question, Answer
from account.models import Profile
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

users = ['admin', 'mod', 'csicska', 'paraszt']

# Votes
upvoting = {
    0: [user for user in users if users.index(user) in (1,2)],
    1: [user for user in users if users.index(user) in ()],
    2: [user for user in users if users.index(user) in ()],
    3: [user for user in users if users.index(user) in (0,1,2)]
}

downvoting = {
    0: [user for user in users if users.index(user) in (3,)],
    1: [user for user in users if users.index(user) in ()],
    2: [user for user in users if users.index(user) in (0,1,3)],
    3: [user for user in users if users.index(user) in ()]
}

class TestModels(TestCase):

    def setUp(self):
        for user in users:
            # Users
            u = User()
            u.username = user
            if users.index(user) == 0:
                u.is_superuser = True
            if users.index(user) < 2:
                u.is_staff = True
            u.save()
            # Profiles
            Profile.objects.create(user=u)


    def test_create_questions(self):
        for i in range(4):
            # Votes
            v = Votes()
            v.save()
            upvote_users = User.objects.filter(username__in=upvoting[i])
            downvote_users = User.objects.filter(username__in=downvoting[i])
            upvote_profiles = Profile.objects.filter(user__in=upvote_users)
            downvote_profiles = Profile.objects.filter(user__in=downvote_users)
            v.upvoters.set(upvote_profiles)
            v.downvoters.set(downvote_profiles)
            v.save()
            # Questions
            Question.objects.create(
                title=fake.text(max_nb_chars=50),
                text=fake.paragraph(nb_sentences=4),
                owner=Profile.objects.get(user__username=users[i]),
                votes=v,
                show_username=True
            )

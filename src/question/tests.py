from django.test import TestCase
from common.models import Comment, Votes
from question.models import Question, Answer
from account.models import Profile
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

users = ['admin', 'mod', 'csicska', 'paraszt']

voting = {
    'up': [
        [user for user in users if users.index(user) in (1,2)],
        [user for user in users if users.index(user) in ()],
        [user for user in users if users.index(user) in ()],
        [user for user in users if users.index(user) in (0,1,2)]
    ],
    'down': [
        [user for user in users if users.index(user) in (3,)],
        [user for user in users if users.index(user) in ()],
        [user for user in users if users.index(user) in (0,1,3)],
        [user for user in users if users.index(user) in ()]
    ]
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
            for upvoter in voting['up'][i]:
                v.upvoters.add(Profile.objects.get(user__username=upvoter))
            for downvoter in voting['down'][i]:
                v.downvoters.add(Profile.objects.get(user__username=downvoter))
            v.save()
            # Questions
            Question.objects.create(
                title=fake.text(max_nb_chars=50),
                text=fake.paragraph(nb_sentences=4),
                owner=Profile.objects.get(user__username=users[i]),
                votes=v,
                show_username=True
            )

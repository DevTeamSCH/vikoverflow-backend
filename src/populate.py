import os
import datetime
import random

import django
from django.core.management import call_command
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vikoverflow.settings.local")
django.setup()

from common.models import Votes  # noqa
from django.contrib.auth.models import User  # noqa
from account.models import Profile  # noqa
from question.models import Question, Answer, Comment  # noqa

call_command('flush')

fake = Faker('hu_HU')
users = []

# Create admin user
admin = User()
admin.username = 'admin'
admin.is_superuser = True
admin.is_staff = True
admin.first_name = 'Admin'
admin.last_name = 'Adminsson'
admin.set_password('admin')
admin.save()
Profile.objects.create(user=User.objects.get(username='admin'))
users.append(admin)

User.objects.create(username='mod', is_staff=True)
users.append('mod')
Profile.objects.create(user=User.objects.get(username='mod'))
User.objects.create(username='csicska')
users.append('csicska')
Profile.objects.create(user=User.objects.get(username='csicska'))


def generate_owner_votes():
    owner = random.choice(users)
    v = Votes()
    v.save()
    upvoters = random.sample(
        users,
        random.randint(0, len(users))
    )
    if owner in upvoters:
        upvoters.remove(owner)
    downvote_choices = [item for item in users if item not in upvoters]
    downvoters = random.sample(
        downvote_choices,
        random.randint(0, len(downvote_choices))
    )
    for u in upvoters:
        v.upvoters.add(Profile.objects.get(user__username=u))
    for u in downvoters:
        v.downvoters.add(Profile.objects.get(user__username=u))
    return {
        'owner': owner,
        'votes': v
    }


# Accounts
for i in range(random.choice(range(3, 9))):
    # Users
    fakedata = fake.simple_profile()
    u = User()
    u.username = fakedata['username']
    name = fakedata['name'].split(' ')
    u.first_name = name[0]
    u.last_name = name[1]
    u.save()
    # Profiles
    Profile.objects.create(user=u)
    users.append(u.username)

# Tags
tag_choices = []
for t in range(random.choice(range(5, 11))):
    tag_choices.append(fake.word())

# Questions
for i in range(random.choice(range(3, 11))):
    ov_q = generate_owner_votes()
    q = Question()
    q.title = fake.text(max_nb_chars=50)
    q.text = fake.paragraph(nb_sentences=4)
    q.owner = Profile.objects.get(user__username=ov_q['owner'])
    q.show_username = bool(random.getrandbits(1))
    q.votes = ov_q['votes']
    q.created_at = datetime.datetime.now()
    q.save()
    for t in random.sample(tag_choices, random.randint(0, len(tag_choices))):
        q.tags.add(t)
    # Comments
    for j in range(random.choice(range(0, 4))):
        ov_cq = generate_owner_votes()
        Comment.objects.create(
            parent_question=q,
            text=fake.paragraph(nb_sentences=4),
            owner=Profile.objects.get(user__username=ov_cq['owner']),
            show_username=bool(random.getrandbits(1)),
            votes=ov_cq['votes']
        )
    # Answers
    accepted_answer = -1
    answer_count = random.choice(range(0, 6))
    has_accepted = bool(random.getrandbits(1))
    if has_accepted and answer_count > 0:
        accepted_answer = random.choice(range(answer_count))
    for k in range(answer_count):
        ov_a = generate_owner_votes()
        a = Answer()
        a.text = fake.paragraph(nb_sentences=4)
        a.owner = Profile.objects.get(user__username=ov_a['owner'])
        a.show_username = bool(random.getrandbits(1))
        if k == accepted_answer:
            a.is_accepted = True
        else:
            a.is_accepted = False
        a.votes = ov_a['votes']
        a.parent = q
        a.save()
        # Comments to answers
        for l in range(random.choice(range(0, 4))):
            ov_ca = generate_owner_votes()
            Comment.objects.create(
                parent_answer=a,
                text=fake.paragraph(nb_sentences=4),
                owner=Profile.objects.get(user__username=ov_ca['owner']),
                show_username=bool(random.getrandbits(1)),
                votes=ov_ca['votes']
            )

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vikoverflow.settings.local")
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

FIXTURES = [
    'users',
    'profiles',
    'questions'
]

for fixture in FIXTURES:
    call_command('loaddata', 'src/vikoverflow/fixtures/' + fixture)

for user in User.objects.all():
        user.set_password(user.password)
        user.save()

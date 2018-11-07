# Generated by Django 2.1 on 2018-10-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downvoters', models.ManyToManyField(related_name='downvotes', to='account.Profile')),
                ('upvoters', models.ManyToManyField(related_name='upvotes', to='account.Profile')),
            ],
        ),
    ]
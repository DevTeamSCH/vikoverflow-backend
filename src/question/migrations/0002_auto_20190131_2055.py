# Generated by Django 2.1.5 on 2019-01-31 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("question", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="deleted",
            field=models.UUIDField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="deleted",
            field=models.UUIDField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="deleted",
            field=models.UUIDField(blank=True, default=None, null=True),
        ),
    ]

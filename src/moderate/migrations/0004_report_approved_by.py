# Generated by Django 2.1.3 on 2019-01-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("account", "0001_initial"), ("moderate", "0003_auto_20181127_0229")]

    operations = [
        migrations.AddField(model_name="report", name="approved_by", field=models.ManyToManyField(to="account.Profile"))
    ]

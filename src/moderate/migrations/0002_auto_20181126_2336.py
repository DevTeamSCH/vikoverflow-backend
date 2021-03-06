# Generated by Django 2.1.3 on 2018-11-26 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("moderate", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="report", name="closed_at", field=models.DateTimeField(null=True)
        ),
        migrations.AlterField(
            model_name="report",
            name="status",
            field=models.CharField(
                choices=[("OPENED", "Opened"), ("CLOSED", "Closed")],
                default="OPENED",
                max_length=255,
            ),
        ),
    ]

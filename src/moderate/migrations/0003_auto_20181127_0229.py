# Generated by Django 2.1.3 on 2018-11-27 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
        ("moderate", "0002_auto_20181126_2336"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.Profile",
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="moderate.Report",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="moderatorcomment", name="owner"),
        migrations.DeleteModel(name="ModeratorComment"),
    ]

# Generated by Django 4.2.13 on 2024-07-22 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app_users", "0003_userdetails_videos_history"),
    ]

    operations = [
        migrations.CreateModel(
            name="TwitterPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, help_text="When this instance was created."
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, help_text="When this instance was modified."
                    ),
                ),
                ("content", models.TextField()),
                (
                    "media_file",
                    models.FileField(
                        blank=True, null=True, upload_to="media/files/twitter_files/"
                    ),
                ),
                ("flag_media_file", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="twitter_posts",
                        to="app_users.userdetails",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]

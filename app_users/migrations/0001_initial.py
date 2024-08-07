# Generated by Django 4.2.13 on 2024-07-15 06:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserDetails",
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
                ("fullname", models.CharField(max_length=350)),
                ("username", models.CharField(max_length=150)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                                message="Email is incorrect",
                            )
                        ],
                    ),
                ),
                (
                    "avatar_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/files/user_avatar_images/",
                    ),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/files/user_cover_images/",
                    ),
                ),
                ("password", models.CharField(max_length=200)),
            ],
            options={"abstract": False,},
        ),
    ]

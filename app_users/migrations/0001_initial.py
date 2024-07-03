# Generated by Django 4.2.13 on 2024-06-18 05:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("base_user", "0001_initial"),
    ]

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
                ("password", models.CharField(max_length=30)),
                (
                    "users",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="app_user",
                        to="base_user.user",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
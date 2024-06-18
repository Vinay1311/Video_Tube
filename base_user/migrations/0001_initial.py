# Generated by Django 4.2.13 on 2024-06-18 05:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                                message="Email is incorrect",
                            )
                        ],
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={"abstract": False,},
        ),
    ]

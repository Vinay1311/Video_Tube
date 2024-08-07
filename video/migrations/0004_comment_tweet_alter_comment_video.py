# Generated by Django 4.2.13 on 2024-07-24 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("twitter", "0002_twitterpost_comments_count_twitterpost_like_counts"),
        ("video", "0003_like_twitter"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="tweet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments_on_tweets",
                to="twitter.twitterpost",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments_on_video",
                to="video.videodetails",
            ),
        ),
    ]

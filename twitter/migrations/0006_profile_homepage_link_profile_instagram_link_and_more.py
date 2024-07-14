# Generated by Django 5.0.6 on 2024-07-07 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_tweet_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]

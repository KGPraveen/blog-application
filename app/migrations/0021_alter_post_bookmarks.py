# Generated by Django 4.2.8 on 2023-12-31 06:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0020_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, default=None, related_name='bookmarked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]

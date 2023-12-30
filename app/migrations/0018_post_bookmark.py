# Generated by Django 4.2.8 on 2023-12-30 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmark',
            field=models.ManyToManyField(blank=True, default=None, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
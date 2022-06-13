# Generated by Django 4.0.5 on 2022-06-13 05:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tours', '0004_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='saved',
            unique_together={('tour', 'user')},
        ),
    ]
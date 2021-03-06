# Generated by Django 4.0.5 on 2022-06-14 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tours', '0010_tourhistory_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTourViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed', to='tours.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='TourHistory',
        ),
    ]

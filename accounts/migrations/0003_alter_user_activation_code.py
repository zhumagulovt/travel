# Generated by Django 4.0.4 on 2022-06-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_code',
            field=models.CharField(max_length=10),
        ),
    ]
# Generated by Django 5.1.2 on 2024-11-13 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 13, 9, 46, 39, 383264, tzinfo=datetime.timezone.utc)),
        ),
    ]
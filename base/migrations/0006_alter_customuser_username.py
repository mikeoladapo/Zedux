# Generated by Django 5.1.2 on 2024-10-24 08:15

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_others_file_coursematerial_other_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='Invalid username', message='username must contain letters , numbers and underscores only', regex='^[a-zA-Z0-9_@#]+$'), base.models.CustomUser.validate_username]),
        ),
    ]

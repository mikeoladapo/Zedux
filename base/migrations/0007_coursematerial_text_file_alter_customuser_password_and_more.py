# Generated by Django 5.1.2 on 2024-10-26 18:33

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursematerial',
            name='text_file',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(8, 'password must not be less the 8'), django.core.validators.RegexValidator(code='The password is not strong enough', message='password must contain letters , numbers and at least underscore,@,and # only', regex='^[a-zA-Z0-9_@#]+$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='Invalid username', message='username must contain letters , numbers and underscores,@,and # only', regex='^[a-zA-Z0-9_@#]+$'), base.models.CustomUser.validate_username]),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-23 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursematerial',
            name='text_file',
        ),
        migrations.AddField(
            model_name='coursematerial',
            name='others_file',
            field=models.FileField(blank=True, null=True, upload_to='course_others'),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-29 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycourse',
            name='status',
        ),
    ]
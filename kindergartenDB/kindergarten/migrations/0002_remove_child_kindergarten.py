# Generated by Django 4.1.4 on 2022-12-12 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kindergarten', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='kindergarten',
        ),
    ]

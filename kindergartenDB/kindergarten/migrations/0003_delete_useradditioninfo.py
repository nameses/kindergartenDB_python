# Generated by Django 4.1.4 on 2022-12-13 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kindergarten', '0002_remove_child_kindergarten'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAdditionInfo',
        ),
    ]

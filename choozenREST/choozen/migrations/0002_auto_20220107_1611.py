# Generated by Django 3.2.9 on 2022-01-07 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choozen', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]

# Generated by Django 3.2.9 on 2022-01-12 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choozen', '0002_alter_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
# Generated by Django 3.2.9 on 2022-04-25 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choozen', '0003_person_picture_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_groups', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_members_per_group', models.IntegerField()),
            ],
        ),
    ]

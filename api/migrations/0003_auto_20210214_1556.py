# Generated by Django 3.1.6 on 2021-02-14 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210207_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'ordering': ['id']},
        ),
    ]

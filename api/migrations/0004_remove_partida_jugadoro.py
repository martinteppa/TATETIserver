# Generated by Django 3.1.7 on 2021-05-11 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210511_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='jugadorO',
        ),
    ]

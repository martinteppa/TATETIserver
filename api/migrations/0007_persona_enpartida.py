# Generated by Django 3.1.7 on 2021-05-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210511_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='enPartida',
            field=models.BooleanField(default=False),
        ),
    ]

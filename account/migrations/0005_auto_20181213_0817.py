# Generated by Django 2.1.2 on 2018-12-13 08:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20181213_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='membership_start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 13, 8, 17, 4, 860348, tzinfo=utc), null=True),
        ),
    ]
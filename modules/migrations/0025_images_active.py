# Generated by Django 2.1 on 2018-08-31 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0024_auto_20180831_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]

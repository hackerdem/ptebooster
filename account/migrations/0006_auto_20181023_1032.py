# Generated by Django 2.1.2 on 2018-10-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='Free', max_length=100),
        ),
    ]

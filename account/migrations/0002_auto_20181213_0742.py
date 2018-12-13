# Generated by Django 2.1.2 on 2018-12-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email', 'user_type', 'is_active'], name='user_idx'),
        ),
    ]

# Generated by Django 2.1.2 on 2018-12-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='membership',
            index=models.Index(fields=['presedence'], name='membership_presendence_idx'),
        ),
    ]

# Generated by Django 2.1.2 on 2018-12-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='questionstatistics',
            index=models.Index(fields=['membership_type', 'question_section', 'is_active'], name='statistics_idx'),
        ),
    ]
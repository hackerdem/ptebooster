# Generated by Django 2.1.2 on 2018-12-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0014_auto_20181213_0746'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='module',
            name='module_idx',
        ),
        migrations.AddIndex(
            model_name='module',
            index=models.Index(fields=['active', 'question_type'], name='module_idx'),
        ),
    ]

# Generated by Django 2.1.2 on 2018-10-15 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0032_auto_20180911_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reorderparagraph',
            name='option_5',
            field=models.TextField(max_length=500),
        ),
    ]
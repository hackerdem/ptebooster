# Generated by Django 2.1 on 2018-08-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0026_auto_20180831_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
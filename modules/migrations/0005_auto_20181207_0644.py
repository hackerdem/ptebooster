# Generated by Django 2.1.2 on 2018-12-07 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0004_auto_20181207_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answershortquestions',
            name='item',
            field=models.CharField(max_length=90, unique=True),
        ),
    ]
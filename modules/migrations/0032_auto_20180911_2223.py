# Generated by Django 2.1 on 2018-09-11 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0031_auto_20180911_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answershortquestions',
            old_name='answer',
            new_name='item',
        ),
    ]
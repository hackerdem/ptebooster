# Generated by Django 2.1.2 on 2018-12-09 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0006_auto_20181207_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='model_answer',
            field=models.TextField(default='a', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='essay',
            name='topic',
            field=models.TextField(max_length=250),
        ),
    ]

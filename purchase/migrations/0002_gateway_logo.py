# Generated by Django 2.1.2 on 2018-12-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gateway',
            name='logo',
            field=models.ImageField(default='a', upload_to='ptebooster/media/icons'),
            preserve_default=False,
        ),
    ]
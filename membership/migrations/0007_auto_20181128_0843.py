# Generated by Django 2.1.2 on 2018-11-28 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_membership_module_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='module_image',
            new_name='image',
        ),
    ]

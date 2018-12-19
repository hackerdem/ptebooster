# Generated by Django 2.1.2 on 2018-12-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['customer'], name='order_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['created_on'], name='order_created_on_idx'),
        ),
    ]
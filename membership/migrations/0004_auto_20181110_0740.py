# Generated by Django 2.1.2 on 2018-11-10 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_auto_20181023_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='member_type',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Diamond', 'Diamond')], default='Basic', max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
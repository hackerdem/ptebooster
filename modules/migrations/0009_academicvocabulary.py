# Generated by Django 2.1 on 2018-08-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0008_auto_20180817_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicVocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=150)),
                ('academic_in_sentence', models.CharField(max_length=300)),
            ],
        ),
    ]

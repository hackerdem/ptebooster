# Generated by Django 2.1.2 on 2018-12-10 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0007_auto_20181209_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='multipleselection',
            name='question',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='model_answer',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='fillinblanks',
            name='answers',
            field=models.CharField(help_text='Enter answers comma seperated.', max_length=300),
        ),
        migrations.AlterField(
            model_name='fillinblanks',
            name='paragraph',
            field=models.TextField(help_text='Copy and paste full paragraph.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='highlightwords',
            name='answers',
            field=models.CharField(help_text='Make sure incorrect word has only one instance in the paragraph. Add all answers comma seperated in this field.', max_length=300),
        ),
        migrations.AlterField(
            model_name='highlightwords',
            name='correct_words',
            field=models.CharField(blank=True, help_text='Make sure correct word has only one instance in the paragraph.Add all correct words comma seperated in this field.', max_length=300),
        ),
        migrations.AlterField(
            model_name='highlightwords',
            name='paragraph',
            field=models.TextField(help_text='In the paragrapgh write incorrect words and correct spelling side by side, incorrect first coreect second.', max_length=800),
        ),
    ]
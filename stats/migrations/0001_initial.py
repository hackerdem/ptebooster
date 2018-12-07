# Generated by Django 2.1.2 on 2018-12-07 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modules', '0001_initial'),
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('is_active', models.BooleanField()),
                ('membership_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Membership')),
                ('question_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modules.QuestionSection')),
                ('related_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modules.Module')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='questionstatistics',
            unique_together={('question_id', 'related_module', 'question_section')},
        ),
    ]

# Generated by Django 3.2.10 on 2022-08-12 10:00

from django.db import migrations, models
import django.db.models.deletion
import english.models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0003_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='english.class', verbose_name='class_name'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='class_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='english.class', verbose_name='Class name'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='days',
            field=english.models.ChoiceArrayField(base_field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]), blank=True, default=list, size=5),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(),
        ),
    ]

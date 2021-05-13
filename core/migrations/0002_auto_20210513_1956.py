# Generated by Django 3.1.6 on 2021-05-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directindicator',
            name='max_number',
        ),
        migrations.RemoveField(
            model_name='directindicator',
            name='min_number',
        ),
        migrations.AddField(
            model_name='directindicator',
            name='post_unit',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='directindicator',
            name='pre_unit',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='indirectindicator',
            name='post_unit',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='indirectindicator',
            name='pre_unit',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]

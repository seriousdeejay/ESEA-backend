# Generated by Django 3.1.6 on 2021-05-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20210511_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='closing_text',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='survey',
            name='welcome_text',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]

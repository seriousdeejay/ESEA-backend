# Generated by Django 3.1.6 on 2021-06-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210612_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indirectindicator',
            name='type',
            field=models.CharField(choices=[('PERFORMANCE', 'performance'), ('SCORING', 'scoring')], default='SCORING', max_length=50),
        ),
    ]

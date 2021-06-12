# Generated by Django 3.1.6 on 2021-06-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210605_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indirectindicator',
            name='datatype',
            field=models.CharField(choices=[('TEXT', 'Text'), ('INTEGER', 'Integer'), ('DOUBLE', 'Double'), ('DATE', 'Date'), ('BOOLEAN', 'boolean'), ('SINGLECHOICE', 'singlechoice'), ('MULTIPLECHOICE', 'multiplechoice')], default='TEXT', max_length=50),
        ),
    ]

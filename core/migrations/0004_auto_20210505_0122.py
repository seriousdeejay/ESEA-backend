# Generated by Django 3.1.6 on 2021-05-04 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210505_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='rate',
            field=models.PositiveSmallIntegerField(default=100),
        ),
    ]

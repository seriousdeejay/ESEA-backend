# Generated by Django 3.1.6 on 2021-05-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210509_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='minThreshold',
            field=models.PositiveSmallIntegerField(default=100, null=True),
        ),
    ]

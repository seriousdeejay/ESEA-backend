# Generated by Django 3.1.6 on 2021-05-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210505_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='rate',
            field=models.PositiveSmallIntegerField(default=100, null=True),
        ),
    ]
# Generated by Django 3.1.6 on 2021-05-11 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20210510_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stakeholdergroup',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]

# Generated by Django 3.1.6 on 2021-05-09 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210509_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='responseType',
            field=models.CharField(choices=[('MULTIPLE', 'Multiple'), ('SINGLE', 'Single')], default='SINGLE', max_length=100),
        ),
        migrations.AlterField(
            model_name='survey',
            name='minThreshold',
            field=models.PositiveSmallIntegerField(default=10, null=True),
        ),
    ]

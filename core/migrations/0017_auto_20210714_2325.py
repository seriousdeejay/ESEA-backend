# Generated by Django 3.1.6 on 2021-07-14 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210714_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('denied', 'denied')], default='pending', max_length=100),
        ),
    ]

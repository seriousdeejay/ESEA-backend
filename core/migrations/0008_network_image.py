# Generated by Django 3.1.6 on 2021-05-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210505_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='image',
            field=models.ImageField(blank=True, default='network/default/sustainability-circle.png', upload_to='network/'),
        ),
    ]
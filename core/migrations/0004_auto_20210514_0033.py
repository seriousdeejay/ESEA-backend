# Generated by Django 3.1.6 on 2021-05-13 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210513_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='close_validation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='instruction',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='max_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='min_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

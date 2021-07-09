# Generated by Django 3.1.6 on 2021-07-08 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210708_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directindicator',
            name='datatype',
            field=models.CharField(choices=[('Text', 'Text'), ('Integer', 'Integer'), ('Double', 'Double'), ('Date', 'Date'), ('Boolean', 'Boolean'), ('singleChoice', 'SingleChoice'), ('multipleChoice', 'MultipleChoice')], default='TEXT', max_length=50),
        ),
    ]

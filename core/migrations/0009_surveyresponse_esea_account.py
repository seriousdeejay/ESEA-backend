# Generated by Django 3.1.6 on 2021-04-04 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210404_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='esea_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='core.eseaaccount'),
        ),
    ]

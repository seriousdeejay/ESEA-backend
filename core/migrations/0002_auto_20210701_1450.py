# Generated by Django 3.1.6 on 2021-07-01 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eseaaccount',
            name='campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_accounts', to='core.campaign'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-04-30 14:41

import core.models.campaign
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=75)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name_prefix', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='A New Campaign', max_length=255)),
                ('image', models.ImageField(blank=True, default='campaign/campaign-default.png', upload_to='campaign/')),
                ('required', models.BooleanField(default=True)),
                ('open_survey_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('close_survey_date', models.DateTimeField(default=core.models.campaign.defaultrespondingwindow)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DirectIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=45)),
                ('min_number', models.IntegerField(null=True)),
                ('max_number', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'direct_indicator',
                'verbose_name_plural': 'direct_indicators',
            },
        ),
        migrations.CreateModel(
            name='EseaAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sufficient_responses', models.BooleanField(default=False)),
                ('response_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisation_accounts', to='core.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ispublic', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ispublic', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('image', models.ImageField(blank=True, default='organisation/sustainability-circle.png', upload_to='organisation/')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('esea_accounts', models.ManyToManyField(blank=True, related_name='organisations', through='core.EseaAccount', to='core.Method')),
            ],
            options={
                'verbose_name': 'organisation',
                'verbose_name_plural': 'organisations',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isMandatory', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('instruction', models.TextField(blank=True, null=True)),
                ('default', models.CharField(blank=True, default='', max_length=255)),
                ('answertype', models.CharField(choices=[('TEXT', 'text'), ('NUMBER', 'number'), ('RADIO', 'radio'), ('CHECKBOX', 'checkbox'), ('SCALE', 'scale')], default='TEXT', max_length=100)),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=75)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name_prefix', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveyrespondents', to='core.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='StakeholderGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'stakeholder_group',
                'verbose_name_plural': 'stakeholder_groups',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('anonymous', models.BooleanField()),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='core.method')),
                ('questions', models.ManyToManyField(related_name='surveys', to='core.DirectIndicator')),
                ('stakeholder_groups', models.ManyToManyField(to='core.StakeholderGroup')),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('esea_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='report', serialize=False, to='core.eseaaccount')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='core.method')),
                ('parent_topic', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_topics', to='core.topic')),
                ('questions', models.ManyToManyField(related_name='topics_of_questions', through='core.DirectIndicator', to='core.Question')),
            ],
            options={
                'verbose_name': 'topic',
                'verbose_name_plural': 'topics',
            },
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=8)),
                ('finished', models.BooleanField(default=False)),
                ('esea_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='core.eseaaccount')),
                ('respondent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='core.respondent')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='core.survey')),
            ],
            options={
                'verbose_name': 'survey_response',
                'verbose_name_plural': 'survey_responses',
            },
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direct_indicator_id', models.IntegerField()),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('survey_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_responses', to='core.surveyresponse')),
            ],
            options={
                'verbose_name': 'question_response',
                'verbose_name_plural': 'question_responses',
            },
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=140)),
                ('value', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.question')),
                ('question_responses', models.ManyToManyField(blank=True, related_name='values', to='core.QuestionResponse')),
            ],
            options={
                'db_table': 'f{AppConfig.name}_question_option',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_of_topic', to='core.topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(through='core.DirectIndicator', to='core.Topic'),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ispublic', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('methods', models.ManyToManyField(blank=True, related_name='networks', to='core.Method')),
                ('organisations', models.ManyToManyField(blank=True, related_name='networks', to='core.Organisation')),
            ],
            options={
                'verbose_name': 'network',
                'verbose_name_plural': 'networks',
            },
        ),
        migrations.AddField(
            model_name='eseaaccount',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.method'),
        ),
        migrations.AddField(
            model_name='eseaaccount',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organisation'),
        ),
        migrations.AddField(
            model_name='directindicator',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direct_indicators', to='core.question'),
        ),
        migrations.AddField(
            model_name='directindicator',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direct_indicators', to='core.topic'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.method'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.network'),
        ),
        migrations.CreateModel(
            name='IndirectIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('formula', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indirect_indicators', to='core.topic')),
            ],
            options={
                'unique_together': {('key', 'topic')},
            },
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('profile_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Название профиля')),
                ('active', models.BooleanField(default=True, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MainData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateField(unique=True)),
                ('arrived', models.SmallIntegerField(null=True)),
                ('hosp', models.SmallIntegerField(null=True)),
                ('refused', models.SmallIntegerField(null=True)),
                ('signout', models.SmallIntegerField(null=True)),
                ('deads', models.SmallIntegerField(null=True)),
                ('reanimation', models.SmallIntegerField(null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['dates'], name='data_mainda_dates_2313a4_idx')],
            },
        ),
        migrations.CreateModel(
            name='PlanNumbers',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='data.profiles', verbose_name='Профиль')),
                ('plan', models.IntegerField(verbose_name='План')),
            ],
            options={
                'verbose_name': 'План',
                'verbose_name_plural': 'Планы профилей',
                'ordering': ['profile'],
                'indexes': [models.Index(fields=['plan'], name='data_plannu_plan_4b3eec_idx')],
            },
        ),
        migrations.CreateModel(
            name='AccumulationOfIncoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateField(auto_now_add=True)),
                ('number', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.profiles')),
            ],
            options={
                'indexes': [models.Index(fields=['number'], name='data_accumu_number_6112ce_idx')],
            },
        ),
    ]

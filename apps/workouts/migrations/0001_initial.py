# Generated by Django 5.1.1 on 2024-09-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('state', models.CharField(blank=True, max_length=32, null=True)),
                ('kilometers', models.DecimalField(decimal_places=2, max_digits=7)),
                ('duration', models.DurationField()),
                ('frequency', models.IntegerField(blank=True, null=True)),
                ('kcal', models.IntegerField(blank=True, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('speed', models.DecimalField(decimal_places=2, editable=False, max_digits=7)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]

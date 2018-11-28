# Generated by Django 2.1.3 on 2018-11-28 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('penalty', models.IntegerField()),
                ('cheat', models.CharField(max_length=32)),
                ('positive', models.BooleanField()),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('success', models.BooleanField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='determinant.Habit')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]

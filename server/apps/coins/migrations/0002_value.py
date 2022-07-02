# Generated by Django 4.0.5 on 2022-06-26 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_code', models.PositiveIntegerField()),
                ('char_code', models.CharField(max_length=5)),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=4, max_digits=6)),
                ('rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coins.rate')),
            ],
        ),
    ]
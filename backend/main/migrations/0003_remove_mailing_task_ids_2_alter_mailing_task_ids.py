# Generated by Django 4.2.1 on 2023-12-24 19:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_mailing_task_ids_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='task_ids_2',
        ),
        migrations.AlterField(
            model_name='mailing',
            name='task_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]

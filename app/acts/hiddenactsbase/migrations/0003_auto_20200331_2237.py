# Generated by Django 2.1.7 on 2020-03-31 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiddenactsbase', '0002_auto_20200324_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectacts',
            name='create_date',
            field=models.DateField(default=datetime.date(2019, 12, 6)),
        ),
        migrations.AlterField(
            model_name='objectacts',
            name='acts_instance_num',
            field=models.CharField(blank=True, max_length=100, verbose_name='Кол-во экземпляров'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-17 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiddenactsbase', '0003_auto_20190417_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectacts',
            name='blow_down_act',
        ),
    ]

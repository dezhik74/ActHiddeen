# Generated by Django 2.1.7 on 2019-04-06 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks14base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ks14act',
            name='owner_delegate_position',
            field=models.CharField(blank=True, max_length=150, verbose_name='Должность предст. собственника'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-07-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiddenactsbase', '0010_objectacts_h_act_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectacts',
            name='h_act_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ном. Акта'),
        ),
        migrations.AddField(
            model_name='objectacts',
            name='s_t_act_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ном. Акта'),
        ),
        migrations.AddField(
            model_name='objectacts',
            name='w_d_act_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ном. Акта'),
        ),
        migrations.AddField(
            model_name='objectacts',
            name='w_p_act_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ном. Акта'),
        ),
    ]

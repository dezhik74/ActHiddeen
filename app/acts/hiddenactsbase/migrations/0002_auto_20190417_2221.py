# Generated by Django 2.1.7 on 2019-04-17 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiddenactsbase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectacts',
            name='contractor_requisite',
            field=models.CharField(default='Свидетельство о государственной регистрации серия 78№007274277 от  02.09.2009, ОГРН 1097847236783, ИНН 7805498649, 198188, г. Санкт-Петербург, ул. Возрождения, д.20, литер А, тел. 242-78-10.', max_length=200, verbose_name='Реквизиты подрядчика'),
        ),
        migrations.AlterField(
            model_name='objectacts',
            name='contractor',
            field=models.CharField(default='Общество с ограниченной ответственностью «Интера».', max_length=300, verbose_name='Подрядчик'),
        ),
    ]

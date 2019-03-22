from django.db import models

# Create your models here.
class Ks14ActIS (models.Model):
    act_date = models.CharField(max_length=20, verbose_name='Дата Акта')
    telephonogramm_date = models.CharField(max_length=20, verbose_name='Дата телефонограммы')
    contractor = models.CharField(max_length=20, verbose_name='Подрядчик без кавычек')
    contractor_delegate_genitive = models.CharField(max_length=50, verbose_name='Представитель подрядчика (род падеж)')
    UK_full = models.CharField(max_length=120, verbose_name='УК полное')
    UK_position_genitive = models.CharField(max_length=30, verbose_name='Представитель УК (род падеж)')
    UK_delegate_genitive = models.CharField(max_length=50, verbose_name='Представитель УК (род падеж)')
    UK_decree_genitive = models.CharField(max_length=100, verbose_name='Основание УК (род падеж)')
    supervisor_OSK_number = models.CharField(max_length=2, verbose_name='инженера ОСК№')
    supervisor_delegate_genitive = models.CharField(max_length=50, verbose_name='Представитель заказчика (род падеж)')
    supervisor_decree_genitive = models.CharField(max_length=40, verbose_name = 'Основание заказчика (род падеж')




from django.db import models
from django.shortcuts import reverse


class ObjectCommon (models.Model):
    address = models.CharField(max_length = 100, verbose_name = 'Адрес')
    district_prepositional = models.CharField(max_length = 20, verbose_name = 'Район (предл падеж)')
    contract_number = models.CharField(max_length=40, verbose_name = '№ Контракта')
    contract_date = models.CharField(max_length=20, verbose_name= 'Дата контракта')

    contractor = models.CharField(max_length=20, verbose_name='Подрядчик без кавычек')
    contractor_address = models.CharField(max_length = 100, verbose_name='Адрес подрядчика')
    contractor_OKPO = models.CharField(max_length=8, verbose_name='ОКПО подрядчика')
    contractor_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. подр.')
    contractor_delegate_genitive = models.CharField(max_length=50, verbose_name='Предст. подр.(род падеж)')

    UK_full = models.CharField(max_length=120, verbose_name='УК полное')
    UK_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. УК')
    UK_delegate_genitive = models.CharField(max_length=50, verbose_name='Предст. УК (род падеж)')
    UK_position_genitive = models.CharField(max_length=100, verbose_name='Должность Предст. УК (род падеж)')
    UK_decree_genitive = models.CharField(max_length=100, verbose_name='Основание УК (род падеж)')

    supervisor_OSK_number = models.CharField(max_length=2, verbose_name='инженера ОСК№')
    supervisor_delegate = models.CharField(max_length = 20, verbose_name= 'Технадзор')
    supervisor_delegate_genitive = models.CharField(max_length=50, verbose_name='Технадзор (род падеж)')
    supervisor_decree_genitive = models.CharField(max_length=40, verbose_name = 'Основание заказчика (род падеж')
    supervisor_decree_dative = models.CharField(max_length=40, verbose_name = 'Основание заказчика (дательн падеж')

    administration_order = models.CharField(max_length=100, verbose_name = 'по распоряжению администр.',
                                            blank = True)

    owner_delegate_position = models.CharField(max_length=150, verbose_name='Должность предст. собственника',
                                               blank=True)
    owner_delegate = models.CharField(max_length=30, verbose_name= 'Представитель Собственника', blank = True)
    owner_delegate_genitive = models.CharField(max_length = 30, verbose_name='Предст. Собственника (род падеж)',
                                               blank=True)
    owner_delegate_decree = models.CharField(max_length=100, verbose_name='Основание предст. собств.', blank = True)
    owner_delegate_decree_genitive = models.CharField(max_length=100, verbose_name='Основание предст. собств. (род. падеж)',
                                                      blank=True)

    administration_delegate_position = models.CharField(max_length = 150, verbose_name= 'Должн. предст. адм.')
    administration_delegate_decree = models.CharField(max_length = 50, verbose_name= 'Основание предст. адм.')
    administration_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. Адм.')

    acts = models.ManyToManyField('ActSpecific', blank=True, related_name='object_common')

    class Meta:
        verbose_name = 'Информация объекта '
        verbose_name_plural = 'Информация объекта '

    def __str__(self):
        return '{}'.format(self.address)

    def copy(self):
        s = self.address
        if len(s) > 93:
            s = s[0:93]
        self.address = 'Копия: ' + s
        new_acts = []
        for act in self.acts.all():
            act.id = None
            act.save()
            new_acts.append(act)
        self.id = None
        self.save()
        for act1 in new_acts:
            self.acts.add(act1)

    def delete_common_obj(self):
        for act in self.acts.all():
            act.delete()
        self.delete()

    def update_object_common (self, cleaned_obj_data, cleaned_act_data):
        self.__dict__.update(cleaned_obj_data[0])
        i = 0
        for act in self.acts.all():
            act.__dict__.update(cleaned_act_data[i])
            i += 1
            act.save()
        self.save()
        return self


class ActSpecific (models.Model):
    system_genitive = models.CharField(max_length = 100, verbose_name = 'система (род падеж)')
    act_number = models.CharField(max_length=1, verbose_name='Номер Акта')
    begin_contract_date = models.CharField(max_length = 20, verbose_name= 'Начало по контракту')
    end_contract_date = models.CharField(max_length = 20, verbose_name= 'Конец по контракту')
    begin_fact_date = models.CharField(max_length = 20, verbose_name= 'Начало по факту')
    act_date = models.CharField(max_length=20, verbose_name='Дата Акта')
    summa = models.CharField(max_length = 20, verbose_name= 'Сумма контракта')
    volume = models.CharField(max_length = 30, verbose_name= 'Объем с ед изм')
    telephonogramm_date = models.CharField(max_length=20, verbose_name='Дата телефонограммы')

    class Meta:
        verbose_name = 'Информация акта '
        verbose_name_plural = 'Информация акта '

    def __str__(self):
        return '№{}, {}, сумма {}'.format(self.act_number, self.system_genitive, self.summa)


class Ks14Act (models.Model):
    address = models.CharField(max_length = 100, verbose_name = 'Адрес')
    district_prepositional = models.CharField(max_length = 20, verbose_name = 'Район (предл падеж)')

    system_genitive = models.CharField(max_length = 100, verbose_name = 'система (род падеж)')

    contract_number = models.CharField(max_length=40, verbose_name = '№ Контракта')
    contract_date = models.CharField(max_length=20, verbose_name= 'Дата контракта')
    begin_contract_date = models.CharField(max_length = 20, verbose_name= 'Начало по контракту')
    end_contract_date = models.CharField(max_length = 20, verbose_name= 'Конец по контракту')
    begin_fact_date = models.CharField(max_length = 20, verbose_name= 'Начало по факту')
    act_date = models.CharField(max_length=20, verbose_name='Дата Акта')
    summa = models.CharField(max_length = 20, verbose_name= 'Сумма контракта')
    volume = models.CharField(max_length = 30, verbose_name= 'Объем с ед изм')
    telephonogramm_date = models.CharField(max_length=20, verbose_name='Дата телефонограммы')
    act_number = models.CharField(max_length=1, verbose_name='Номер Акта')

    contractor = models.CharField(max_length=20, verbose_name='Подрядчик без кавычек')
    contractor_address = models.CharField(max_length = 100, verbose_name='Адрес подрядчика')
    contractor_OKPO = models.CharField(max_length=8, verbose_name='ОКПО подрядчика')
    contractor_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. подр.')
    contractor_delegate_genitive = models.CharField(max_length=50, verbose_name='Предст. подр.(род падеж)')

    UK_full = models.CharField(max_length=120, verbose_name='УК полное')
    UK_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. УК')
    UK_delegate_genitive = models.CharField(max_length=50, verbose_name='Предст. УК (род падеж)')
    UK_position_genitive = models.CharField(max_length=100, verbose_name='Должность Предст. УК (род падеж)')
    UK_decree_genitive = models.CharField(max_length=100, verbose_name='Основание УК (род падеж)')

    supervisor_OSK_number = models.CharField(max_length=2, verbose_name='инженера ОСК№')
    supervisor_delegate = models.CharField(max_length = 20, verbose_name= 'Технадзор')
    supervisor_delegate_genitive = models.CharField(max_length=50, verbose_name='Технадзор (род падеж)')
    supervisor_decree_genitive = models.CharField(max_length=40, verbose_name = 'Основание заказчика (род падеж')
    supervisor_decree_dative = models.CharField(max_length=40, verbose_name = 'Основание заказчика (дат падеж')

    administration_order = models.CharField(max_length=100, verbose_name = 'по распоряжению администр.',
                                            blank = True)

    owner_delegate_position = models.CharField(max_length=150, verbose_name='Должность предст. собственника',
                                               blank=True)
    owner_delegate = models.CharField(max_length=30, verbose_name= 'Представитель Собственника', blank = True)
    owner_delegate_genitive = models.CharField(max_length = 30, verbose_name='Предст. Собственника (род падеж)',
                                               blank=True)
    owner_delegate_decree = models.CharField(max_length=100, verbose_name='Основание предст. собств.', blank = True)
    owner_delegate_decree_genitive = models.CharField(max_length=100, verbose_name='Основание предст. собств. (род. падеж)',
                                                      blank=True)

    administration_delegate_position = models.CharField(max_length = 150, verbose_name= 'Должн. предст. адм.')
    administration_delegate_decree = models.CharField(max_length = 50, verbose_name= 'Основание предст. адм.')
    administration_delegate = models.CharField(max_length = 20, verbose_name= 'Предст. Адм.')

    class Meta:
        verbose_name = 'Финдоки старая версия'
        verbose_name_plural = 'Финдоки старая версия'

    def __str__(self):
        return '{} -> {}'.format(self.address, self.system_genitive)

    def get_absolute_url(self):
        return reverse('ks14_object_detail_url', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('ks14_object_edit_url', kwargs={'pk': self.pk})




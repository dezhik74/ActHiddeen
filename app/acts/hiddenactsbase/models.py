from django.db import models
from django.shortcuts import reverse
import re


class HiddenActIS (models.Model):
    act_number = models.CharField(max_length=20, verbose_name='Ном. Акта', blank=True)
    act_date = models.CharField(max_length=50, verbose_name='Дата Акта')
    presented_work = models.CharField(max_length=200, verbose_name='Предъявл.')
    materials = models.CharField(max_length=200, verbose_name='Материалы')
    permitted_work = models.CharField(max_length=200, verbose_name='Разрешено')
    begin_date = models.CharField(max_length=50, verbose_name='От:')
    end_date = models.CharField(max_length=50, verbose_name='До:')
    work_SNIP = models.CharField(max_length=100, verbose_name='СНИП:')

    class Meta:
        ordering = ['act_number']
        verbose_name = 'Акт скрытых инженерка '

    def __str__(self):
        return '{} -> {}'.format(self.act_number, self.presented_work)


class BlowDownAct (models.Model):
    act_number = models.CharField(max_length=20, verbose_name='Ном. Акта', blank=True)
    act_date = models.CharField(max_length=50, verbose_name='Дата Акта')
    trassa = models.CharField(max_length=150, verbose_name='Трасса',
                              default='от отключающего устройства Д=     мм розлив холодного водоснабжения')
    trassa_lenght = models.CharField(max_length=10, verbose_name='Длина трассы')
    purge_method = models.CharField(max_length=150, verbose_name='Метод продувки',
                                    default='сетевой водой ХВС не менее 2-3 раз объема системы до "светлой воды"')

    class Meta:
        verbose_name = 'Акт промыки (продувки)'

    def __str__(self):
        return '{} -> Промывка (продувка)'.format(self.act_number)

class ObjectActs (models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=False)
    system_type = models.CharField(max_length=100, verbose_name='тип')
    designer = models.CharField(max_length=200, verbose_name='Проектант')
    contractor = models.CharField(max_length=300, verbose_name='Подрядчик',
                                  default='Общество с ограниченной ответственностью «Интера».')
    contractor_requisite = models.CharField(max_length= 200, verbose_name='Реквизиты подрядчика',
                                    default= 'Свидетельство о государственной регистрации серия 78' +
                                             '№007274277 от  02.09.2009, ОГРН 1097847236783, ' +
                                             'ИНН 7805498649, 198188, г. Санкт-Петербург,' +
                                             ' ул. Возрождения, д.20, литер А, тел. 242-78-10.')
    supervisor_engineer = models.CharField(max_length=100, verbose_name='Технадзор')
    contractor_engineer = models.CharField(max_length=100, verbose_name='Прораб')
    designer_engineer = models.CharField(max_length=100, verbose_name='Проектировщик')
    project_number = models.CharField(max_length=100, verbose_name='Ном. проекта')
    exec_documents = models.CharField(max_length=100, verbose_name='Исполн.')
    supervisor_engineer_decree = models.CharField(max_length=100, verbose_name='Приказ технадзора')
    contractor_engineer_decree = models.CharField(max_length=100, verbose_name='Приказ прораба')
    designer_engineer_decree = models.CharField(max_length=100, verbose_name='Приказ проектировщика')
    acts = models.ManyToManyField('HiddenActIS', blank=True, related_name='object_acts')
    blow_down_act = models.ForeignKey('BlowDownAct', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Набор актов объекта '

    def __str__(self):
        return '{}'.format(", ".join([self.system_type, self.address]))

    def get_absolute_url(self):
        return reverse('object_detail_url', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('object_edit_url', kwargs={'pk': self.pk})

    def get_20_chars_of_contractor(self):
        return self.contractor[0:20] + '...'

    def get_short_contractor(self):
        s = re.findall(r"[\"\«\»\']\D+?[\"\«\»\']", self.contractor)
        if len(s) == 0:
            return self.contractor
        else:
            return s[0]

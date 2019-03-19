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

    class Meta:
        ordering = ['act_number']
        verbose_name = 'Акт скрытых инженерка '

    def __str__(self):
        return '{} -> {}'.format(self.act_number, self.presented_work)


class ObjectActs (models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=False)
    system_type = models.CharField(max_length=100, verbose_name='тип')
    designer = models.CharField(max_length=200, verbose_name='Проектант')
    contractor = models.CharField(max_length=300, verbose_name='Подрядчик',
                                  default= 'Общество с ограниченной ответственностью «Интера».' +
                                           'Свидетельство о государственной регистрации серия 78'+
                                           '№007274277 от  02.09.2009, ОГРН 1097847236783, ИНН 7805498649,'+
                                           '198188, г. Санкт-Петербург, ул. Возрождения, д.20, литер А, тел. 242-78-10.')
    supervisor_engineer = models.CharField(max_length=100, verbose_name='Технадзор')
    contractor_engineer = models.CharField(max_length=100, verbose_name='Прораб')
    project_number = models.CharField(max_length=100, verbose_name='Ном. проекта')
    exec_documents = models.CharField(max_length=100, verbose_name='Исполн.')
    supervisor_engineer_decree = models.CharField(max_length=100, verbose_name=' ')
    contractor_engineer_decree = models.CharField(max_length=100, verbose_name=' ')
    acts = models.ManyToManyField('HiddenActIS', blank=True, related_name='object_acts')

    class Meta:
        verbose_name = 'Набор актов объекта '

    def __str__(self):
        return '{}'.format(", ".join([self.system_type, self.address]))

    def get_absolute_url(self):
        return reverse('object_detail_url', kwargs={'pk':self.pk})

    def get_edit_url(self):
        return reverse('object_edit_url', kwargs={'pk':self.pk})

    def get_20_chars_of_contractor(self):
        return self.contractor[0:20] + '...'

    def get_short_contractor (self):
        s=re.findall(r"[\"\«\»\']\D+?[\"\«\»\']", self.contractor)
        if len(s) == 0:
            return self.contractor
        else:
            return s[0]



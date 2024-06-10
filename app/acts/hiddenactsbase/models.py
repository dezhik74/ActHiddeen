import pprint

from django.db import models
from django.shortcuts import reverse
import re
from datetime import date


class HiddenActIS(models.Model):
    act_number = models.CharField(max_length=20, verbose_name='Ном. Акта', blank=True)
    act_date = models.CharField(max_length=50, verbose_name='Дата Акта')
    presented_work = models.CharField(max_length=500, verbose_name='Предъявл.')
    materials = models.CharField(max_length=500, verbose_name='Материалы')
    permitted_work = models.CharField(max_length=500, verbose_name='Разрешено')
    begin_date = models.CharField(max_length=50, verbose_name='От:')
    end_date = models.CharField(max_length=50, verbose_name='До:')
    work_SNIP = models.CharField(max_length=500, verbose_name='СНИП:', blank=True)
    docs = models.CharField(max_length=500, verbose_name='Предьявлены документы',
                            default='исполнительная схема, сертификаты/свителельства', blank=True)
    annex = models.CharField(max_length=500, verbose_name='Приложения', blank=True)
    certificates = models.ManyToManyField(to='Certificate', related_name='acts', verbose_name='Сертификаты', blank=True)

    class Meta:
        ordering = ['act_number']
        verbose_name = 'Акт скрытых'
        verbose_name_plural = 'Акты скрытых'

    def __str__(self):
        return f'[{self.id}] {self.act_number} -> {self.presented_work}'


class ObjectActs(models.Model):
    create_date = models.DateField(blank=False, default=date(2019, 12, 6))
    address = models.CharField(max_length=500, verbose_name='Адрес', blank=False)
    system_type = models.CharField(max_length=500, verbose_name='тип')
    designer = models.CharField(max_length=500, verbose_name='Проектант')
    contractor = models.CharField(max_length=500, verbose_name='Подрядчик',
                                  default='Общество с ограниченной ответственностью «Интера».')
    contractor_requisite = models.CharField(max_length=500, verbose_name='Реквизиты подрядчика',
                                            default='Свидетельство о государственной регистрации серия 78' +
                                                    '№007274277 от  02.09.2009, ОГРН 1097847236783, ' +
                                                    'ИНН 7805498649, 198188, г. Санкт-Петербург,' +
                                                    ' ул. Возрождения, д.20, литер А, тел. 242-78-10.')
    supervisor_engineer = models.CharField(max_length=200, verbose_name='Технадзор')
    contractor_engineer = models.CharField(max_length=200, verbose_name='Прораб')
    contractor_supervisor = models.CharField(max_length=200, verbose_name='Технадзор наш', blank=True)
    designer_engineer = models.CharField(max_length=200, verbose_name='Проектировщик', blank=True)
    service_engineer = models.CharField(max_length=200, verbose_name='От УК', blank=True)
    project_number = models.CharField(max_length=100, verbose_name='Ном. проекта')
    exec_documents = models.CharField(max_length=500, verbose_name='Исполн.')
    supervisor_engineer_decree = models.CharField(max_length=200, verbose_name='Приказ технадзора')
    contractor_engineer_decree = models.CharField(max_length=200, verbose_name='Приказ прораба')
    contractor_supervisor_decree = models.CharField(max_length=200, verbose_name='Приказ технадз. наш', blank=True)
    designer_engineer_decree = models.CharField(max_length=200, verbose_name='Приказ проектировщика', blank=True)
    acts_instance_num = models.CharField(max_length=100, verbose_name='Кол-во экземпляров', blank=True)
    acts = models.ManyToManyField('HiddenActIS', blank=True, related_name='object_acts')
    # Дополнительные акты
    # Акт промывки/продувки (w_p_act)
    is_washing_purging_act = models.BooleanField(default=False, verbose_name='Продувка')
    w_p_act_number = models.CharField(max_length=20, verbose_name='Номер', blank=True)
    w_p_act_date = models.CharField(max_length=50, verbose_name='Дата', default='"15" июня 2022 г.')
    # Акт промывки/дезинфекции (w_d_act)
    is_washing_disinfection_act = models.BooleanField(default=False, verbose_name='Дезинфекция')
    w_d_act_number = models.CharField(max_length=20, verbose_name='Номер', blank=True)
    w_d_act_date = models.CharField(max_length=50, verbose_name='Дата', default='"15" июня 2022 г.')
    w_d_disinfection_protocol_1 = models.CharField(
        max_length=200, verbose_name='Анализ воды 1', default='А0806/64 от 15.06.2022 г.'
    )
    w_d_disinfection_protocol_2 = models.CharField(
        max_length=200, verbose_name='Анализ воды 2', default='4465/2022 от 10.06.2022 г.'
    )
    # Акт гидравлики (h_act)
    is_hydraulic_testing_act = models.BooleanField(default=False, verbose_name='Гидравлика')
    h_act_number = models.CharField(max_length=20, verbose_name='Номер', blank=True)
    h_act_date = models.CharField(max_length=50, verbose_name='Дата', default='"15" июня 2022 г.')
    # Акт испытания канализации (s_t_act)
    is_sewer_testing_act = models.BooleanField(default=False, verbose_name='Испыт. канализации')
    s_t_act_number = models.CharField(max_length=20, verbose_name='Номер', blank=True)
    s_t_act_date = models.CharField(max_length=50, verbose_name='Дата', default='"15" июня 2022 г.')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return '{}'.format(", ".join([self.system_type, self.address]))

    def get_absolute_url(self):
        return reverse('object_detail_url', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('object_edit_url', kwargs={'pk': self.pk})

    def get_20_chars_of_contractor(self):
        return self.contractor[0:20] + '...'

    def get_short_contractor(self):
        """
        Дает короткое имя подрядчика - извлекает из кавычек
        """
        s = re.findall(r"[\"\«\»\']\D+?[\"\«\»\']", self.contractor)
        if len(s) == 0:
            return self.contractor
        else:
            return s[0]

    def update_obj(self, cleaned_obj_data, cleaned_act_data):
        self.__dict__.update(cleaned_obj_data[0])
        # заменяем
        for act in self.acts.all():
            if len(cleaned_act_data) > 0:
                new_act_data = cleaned_act_data.pop()
                act.__dict__.update(new_act_data)
                if act.certificates.count() > 0:
                    for cert in act.certificates.all():
                        act.certificates.remove(cert)
                for new_cert in new_act_data["certificates"]:
                    act.certificates.add(new_cert)
                act.save()
                # print('change', act.pk)
            else:
                # print('delete', act.pk)
                act.delete()
        # создаем новые
        for act_data in cleaned_act_data:
            new_cert_list = act_data.pop('certificates')
            new_act = self.acts.create(**act_data)
            for new_cert in new_cert_list:
                new_act.certificates.add(new_cert)
            new_act.save()
        self.save()
        return self


class Certificate(models.Model):
    filename = models.FileField(upload_to='certificates/', verbose_name='Файл')
    description = models.CharField(max_length=100, verbose_name='Описание')
    year = models.CharField(max_length=4, verbose_name='Год')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['-year', 'description']

    def __str__(self):
        return f'[{self.year}] {self.description}'


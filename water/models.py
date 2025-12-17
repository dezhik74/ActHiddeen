from django.db import models

class WaterAssay (models.Model):
    # Заключение
    conclusion_date=models.DateField(verbose_name="Дата заключения", null=True, blank=True)
    customer = models.CharField(verbose_name="Заказчик", max_length=50, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, blank=True)
    # Акт приема проб воды
    act_number = models.CharField(verbose_name="Номер акта", max_length=20, blank=True)
    act_date = models.DateField(verbose_name="Дата акта", null=True, blank=True)
    hvs_probe_number = models.CharField(verbose_name="Номер пробы ХВС", max_length=50, blank=True)
    gvs_probe_number = models.CharField(verbose_name="Номер пробы ГВС", max_length=50, blank=True)
    probe_date = models.DateField(verbose_name="Дата отбора проб", null=True, blank=True)
    # Протокол испытаний - химия
    chemistry_number = models.CharField(verbose_name="Номер протокола химии", max_length=20, blank=True)
    chemistry_date = models.DateField(verbose_name="Дата протокола химии", null=True, blank=True)
    chemistry_order_number = models.CharField(verbose_name="Номер заявки на химию", max_length=20, blank=True)
    chemistry_order_date = models.DateField(verbose_name="Дата заявки на химию", null=True, blank=True)
    # Протокол исследования - биология
    bio_number = models.CharField(verbose_name="Номер протокола био", max_length=20, blank=True)
    bio_date = models.DateField(verbose_name="Дата протокола био", null=True, blank=True)
    hvs_bio_code = models.CharField(verbose_name="Код пробы ХВС", max_length=20, blank=True)
    gvs_bio_code = models.CharField(verbose_name="Код пробы ГВС", max_length=20, blank=True)
    hvs_bio_referral = models.CharField(verbose_name="Направление ХВС био", max_length=20, blank=True)
    gvs_bio_referral = models.CharField(verbose_name="Направление ГВС био", max_length=20, blank=True)
    bio_begin_date = models.DateField(verbose_name="Дата начала испытаний", null=True, blank=True)
    bio_end_date = models.DateField(verbose_name="Дата конца испытаний", null=True, blank=True)
    # Показатели хим анализа
    hvs_ph = models.CharField(verbose_name="ХВС ph", max_length=20, blank=True)
    hvs_fe = models.CharField(verbose_name="ХВС fe", max_length=20, blank=True)
    hvs_turb = models.CharField(verbose_name="ХВС Мутн.", max_length=20, blank=True)
    hvs_chroma = models.CharField(verbose_name="ХВС Цветн.", max_length=20, blank=True)
    hvs_rig = models.CharField(verbose_name="ХВС Жестк.", max_length=20, blank=True)
    hvs_ox = models.CharField(verbose_name="ХВС Окисл.", max_length=20, blank=True)
    gvs_ph = models.CharField(verbose_name="ГВС ph", max_length=20, blank=True)
    gvs_fe = models.CharField(verbose_name="ГВС fe", max_length=20, blank=True)
    gvs_turb = models.CharField(verbose_name="ГВС Мутн.", max_length=20, blank=True)
    gvs_chroma = models.CharField(verbose_name="ГВС Цветн.", max_length=20, blank=True)
    gvs_rig = models.CharField(verbose_name="ГВС Жестк.", max_length=20, blank=True)
    gvs_ox = models.CharField(verbose_name="ГВС Окисл.", max_length=20, blank=True)

    class Meta:
        verbose_name = "Анализ воды"
        verbose_name_plural = "Анализы воды"
        ordering = ['-id']

    def is_fully_filled(self):
        """
        Возвращает True, если ВСЕ поля (кроме id и pk) имеют значение
        """
        for field in self._meta.fields:
            if field.name == 'id':
                continue
            value = getattr(self, field.name)
            # Проверяем на пустоту: None, пустая строка, пустая дата и т.д.
            if value in (None, '', [], {}):
                return False
            # Для дат — дополнительно проверяем на минимальную дату (если поле пустое, Django может вернуть None)
            if isinstance(field, models.DateField) and value is None:
                return False
        return True

    def __str__(self):
        return f"[{self.customer}] [{self.address}] [{str(self.conclusion_date)}]"

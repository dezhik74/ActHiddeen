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

    class Meta:
        verbose_name = "Анализ воды"
        verbose_name_plural = "Анализы воды"
        ordering = ['-id']

    def __str__(self):
        return f"[{self.customer}] [{self.address}] [{str(self.conclusion_date)}]"

# water/admin.py

from django.contrib import admin
from .models import WaterAssay


@admin.register(WaterAssay)
class WaterAssayAdmin(admin.ModelAdmin):
    list_display = (
        'conclusion_date',
        'customer',
        'address',
    )
    list_filter = (
        'conclusion_date',
        'customer',
        'address',
    )
    search_fields = (
        'customer',
        'address',
    )
    date_hierarchy = 'conclusion_date'

    fieldsets = (
        ("Заключение", {
            'fields': ('conclusion_date', 'customer', 'address')
        }),
        ("Акт приёма проб воды", {
            'fields': ('act_number', 'act_date', 'probe_date', 'hvs_probe_number', 'gvs_probe_number')
        }),
        ("Протокол химических испытаний", {
            'fields': (('chemistry_number', 'chemistry_date'), ('chemistry_order_number', 'chemistry_order_date'))
        }),
        ("Протокол биологических исследований", {
            'fields': (
                ('bio_number', 'bio_date'),
                ('hvs_bio_code', 'gvs_bio_code'),
                ('hvs_bio_referral', 'gvs_bio_referral'),
                ('bio_begin_date', 'bio_end_date'),
            )
        }),
    )

    ordering = ('-id',)
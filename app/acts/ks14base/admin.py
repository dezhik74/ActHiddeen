from django.contrib import admin
from .models import *

# Register your models here.

class Ks14Admin (admin.ModelAdmin):
    class Meta:
        model = Ks14Act

    save_as = True
    list_display = ('address', 'contract_number', 'district_prepositional', 'system_genitive', 'summa')
    fields = (
              'address',
              ('district_prepositional','district_genitive'),
              'system_genitive',
              ('contract_number', 'contract_date'),
              ('begin_contract_date', 'end_contract_date'),
              ('begin_fact_date', 'act_date'),
              ('summa', 'volume'),
              ('telephonogramm_date', 'act_number'),
              ('contractor', 'contractor_address'),
              'contractor_OKPO',
              ('contractor_delegate', 'contractor_delegate_genitive'),
              'UK_full',
              ('UK_delegate', 'UK_delegate_genitive'),
              ('UK_position_genitive', 'UK_decree_genitive'),
              'supervisor_OSK_number',
              ('supervisor_delegate', 'supervisor_delegate_genitive'),
              ('supervisor_decree_genitive', 'supervisor_decree_dative'),
              'administration_order',
              ('owner_delegate', 'owner_delegate_genitive'),
              'owner_delegate_position',
              ('owner_delegate_decree', 'owner_delegate_decree_genitive'),
              'administration_delegate_position',
              ('administration_delegate_decree', 'administration_delegate'),
              )

class ActSpecificInline (admin.TabularInline):
    model = ObjectCommon.acts.through


class ObjectCommonAdmin (admin.ModelAdmin):
    class Meta:
        model = ObjectCommon

    save_as = True
    list_display = ('address', 'contract_number', 'district_prepositional')
    inlines = [ActSpecificInline]
    fields = (
                'address',
                ('district_prepositional','district_genitive'),
                ('contract_number', 'contract_date'),
                ('contractor', 'contractor_address'),
                'contractor_OKPO',
                ('contractor_delegate', 'contractor_delegate_genitive'),
                'UK_full',
                ('UK_delegate', 'UK_delegate_genitive'),
                ('UK_position_genitive', 'UK_decree_genitive'),
                'supervisor_OSK_number',
                ('supervisor_delegate', 'supervisor_delegate_genitive'),
                ('supervisor_decree_genitive', 'supervisor_decree_dative'),
                'administration_order',
                ('owner_delegate', 'owner_delegate_genitive'),
                'owner_delegate_position',
                ('owner_delegate_decree', 'owner_delegate_decree_genitive'),
                'administration_delegate_position',
                ('administration_delegate_decree', 'administration_delegate'),
              )


class ActSpecificAdmin (admin.ModelAdmin):
    class Meta:
        model = ActSpecific

    save_as = True
    # list_display = ('address', 'contract_number', 'district_prepositional')
    fields = (
        ('act_number', 'system_genitive'),
        ('begin_contract_date', 'end_contract_date'),
        ('begin_fact_date', 'act_date'),
        ('summa', 'volume'),
        'telephonogramm_date',
    )


admin.site.register(Ks14Act, Ks14Admin)
admin.site.register(ObjectCommon, ObjectCommonAdmin)
admin.site.register(ActSpecific, ActSpecificAdmin)


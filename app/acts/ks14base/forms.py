from django.forms import ModelForm
from .models import *


class ObjectCommonForm (ModelForm):
    class Meta:
        model = ObjectCommon
        fields = [
            'address',
            'district_prepositional', 'district_genitive',
            'contract_number', 'contract_date',
            'contractor', 'contractor_address',
            'contractor_OKPO',
            'contractor_delegate', 'contractor_delegate_genitive',
            'UK_full',
            'UK_delegate', 'UK_delegate_genitive',
            'UK_position_genitive', 'UK_decree_genitive',
            'supervisor_OSK_number',
            'supervisor_delegate', 'supervisor_delegate_genitive',
            'supervisor_decree_genitive', 'supervisor_decree_dative',
            'administration_order',
            'owner_delegate', 'owner_delegate_genitive',
            'owner_delegate_position',
            'owner_delegate_decree', 'owner_delegate_decree_genitive',
            'administration_delegate_position',
            'administration_delegate_decree', 'administration_delegate',
              ]
        error_css_class = "alert alert-danger mb-0 py-0"

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'


class ActSpecificForm (ModelForm):
    class Meta:
        model = ActSpecific
        fields = [
            'act_number', 'system_genitive',
            'begin_contract_date', 'end_contract_date',
            'begin_fact_date', 'act_date',
            'summa', 'volume',
            'telephonogramm_date',
              ]
        error_css_class = "alert alert-danger mb-0 py-0"

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'
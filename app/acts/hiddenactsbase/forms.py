from django import forms
from django.forms import ModelForm

from .models import *


class EditObjectBaseForm (ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f.startswith('is') :
                self.fields[f].widget.attrs['class'] = 'form-control-sm'
            else:
                self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'


class ObjectForm (EditObjectBaseForm):
    class Meta:
        model = ObjectActs
        exclude = ['create_date', 'acts']
        # fields = [
        #     'address', 'system_type', 'designer', 'contractor', 'contractor_requisite', 'supervisor_engineer',
        #     'designer_engineer', 'contractor_engineer', 'project_number', 'exec_documents',
        #     'supervisor_engineer_decree', 'contractor_engineer_decree', 'designer_engineer_decree',
        #     'acts_instance_num'
        # ]

        error_css_class = "alert alert-danger mb-0 py-0"


class HActISForm(EditObjectBaseForm):
    class Meta:
        model = HiddenActIS
        fields = [
            'act_number', 'act_date', 'presented_work', 'materials',
            'permitted_work', 'begin_date', 'end_date', 'work_SNIP',
            'docs', 'annex'
        ]


class SearchForm (forms.Form):
    search_object = forms.CharField (max_length=100)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['search_object'].widget.attrs['class'] = 'align-self-center form-control-sm mr-sm-2'
        self.fields['search_object'].widget.attrs['placeholder'] = 'Поиск по объектам'


from django import forms
from django.forms import ModelForm

from .models import *


class ObjectForm (ModelForm):
    class Meta:
        model = ObjectActs
        fields = [
            'address', 'system_type', 'designer', 'contractor', 'contractor_requisite','supervisor_engineer',
            'designer_engineer', 'contractor_engineer', 'project_number', 'exec_documents',
            'supervisor_engineer_decree', 'contractor_engineer_decree', 'designer_engineer_decree'
        ]

        error_css_class = "alert alert-danger mb-0 py-0"

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'system_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'designer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_requisite': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '"2"'}),
            'supervisor_engineer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'designer_engineer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'project_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'exec_documents': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'supervisor_engineer_decree': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer_decree': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'designer_engineer_decree': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class HActISForm(ModelForm):
    class Meta:
        model = HiddenActIS
        fields = [
            'act_number', 'act_date', 'presented_work', 'materials',
            'permitted_work', 'begin_date', 'end_date', 'work_SNIP'
        ]
        widgets = {
            'act_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'act_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'presented_work': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'materials': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'permitted_work': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'begin_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'work_SNIP': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class BlowDownActForm(ModelForm):
    class Meta:
        model = BlowDownAct
        fields = ['act_number','act_date', 'trassa','trassa_lenght', 'purge_method']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'


class SearchForm (forms.Form):
    search_object = forms.CharField (max_length=100)


    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['search_object'].widget.attrs['class'] = 'align-self-center form-control-sm mr-sm-2'
        self.fields['search_object'].widget.attrs['placeholder'] = 'Поиск по объектам'


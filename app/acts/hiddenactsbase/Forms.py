from django import forms
from django.forms import ModelForm

from .models import ObjectActs, HiddenActIS


class ObjectForm (ModelForm):
    class Meta:
        model = ObjectActs
        fields = [
            'address', 'system_type', 'designer', 'contractor', 'supervisor_engineer',
            'contractor_engineer', 'project_number', 'exec_documents',
            'supervisor_engineer_decree', 'contractor_engineer_decree'
        ]

        error_css_class = "alert alert-danger mb-0 py-0"

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'system_type': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'designer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '"2"'}),
            'supervisor_engineer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'project_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'exec_documents': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'supervisor_engineer_decree': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer_decree': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class HActISForm(ModelForm):
    class Meta:
        model = HiddenActIS
        fields = [
            'act_number', 'act_date', 'presented_work', 'materials',
            'permitted_work', 'begin_date', 'end_date'
        ]
        widgets = {
            'act_number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'act_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'presented_work': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'materials': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'permitted_work': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'begin_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

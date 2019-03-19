from django import forms
from django.forms import ModelForm
from .models import ObjectActs, HiddenActIS
from django.shortcuts import get_object_or_404


class ObjectForm (ModelForm):
    class Meta:
        model=ObjectActs
        fields = [
            'address', 'system_type', 'designer', 'contractor','supervisor_engineer',
            'contractor_engineer', 'project_number', 'exec_documents',
            'supervisor_engineer_decree', 'contractor_engineer_decree'
        ]

        widgets = {
            'address' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'system_type' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'designer' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor' : forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '"2"'}),
            'supervisor_engineer' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'project_number' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'exec_documents' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'supervisor_engineer_decree' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'contractor_engineer_decree' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),

        }

    # def update (self, pk):
    #     changing_obj = get_object_or_404(ObjectActs, pk=pk)
    #     changing_obj.address = self.cleaned_data['address']
    #     changing_obj.system_type = self.cleaned_data['system_type']
    #     changing_obj.designer = self.cleaned_data['designer']
    #     changing_obj.supervisor_engineer = self.cleaned_data['supervisor_engineer']
    #     changing_obj.contractor_engineer = self.cleaned_data['contractor_engineer']
    #     changing_obj.project_number = self.cleaned_data['project_number']
    #     changing_obj.exec_documents = self.cleaned_data['exec_documents']
    #     changing_obj.supervisor_engineer_decree = self.cleaned_data['supervisor_engineer_decree']
    #     changing_obj.contractor_engineer_decree = self.cleaned_data['contractor_engineer_decree']
    #     changing_obj.save()
    #     return changing_obj


class HActISForm(ModelForm):
    class Meta:
        model=HiddenActIS
        fields = [
            'act_number','act_date','presented_work','materials',
            'permitted_work','begin_date','end_date'
        ]
        widgets = {
            'act_number' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'act_date' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'presented_work' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'materials' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'permitted_work' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'begin_date' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'end_date' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

    # def update(self, pk):
    #     changing_obj = get_object_or_404(HiddenActIS, pk=pk)
    #     changing_obj.act_number = self.cleaned_data['act_number']
    #     changing_obj.act_date = self.cleaned_data['act_date']
    #     changing_obj.presented_work = self.cleaned_data['presented_work']
    #     changing_obj.materials = self.cleaned_data['materials']
    #     changing_obj.permitted_work = self.cleaned_data['permitted_work']
    #     changing_obj.begin_date = self.cleaned_data['begin_date']
    #     changing_obj.end_date = self.cleaned_data['end_date']
    #     changing_obj.save()
    #     return changing_obj

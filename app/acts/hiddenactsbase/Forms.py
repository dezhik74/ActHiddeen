from django import forms
from .models import ObjectActs, HiddenActIS
from django.shortcuts import get_object_or_404


class ObjectForm (forms.Form):
    address = forms.CharField(max_length=100, label='Объект')
    system_type = forms.CharField(max_length=100, label='кап.рем.')
    designer=forms.CharField(max_length=200, label='Проектант')
    supervisor_engineer=forms.CharField(max_length=100, label='Технадзор')
    contractor_engineer=forms.CharField(max_length=100, label='Прораб')
    project_number=forms.CharField(max_length=100, label='Ном.проекта')
    exec_documents=forms.CharField(max_length=100, label='Исп.док.')
    supervisor_engineer_decree=forms.CharField(max_length=100, label='основан.')
    contractor_engineer_decree=forms.CharField(max_length=100, label='основан.')

    address.widget.attrs.update({'class': 'form-control form-control-sm'})
    system_type.widget.attrs.update({'class': 'form-control form-control-sm'})
    designer.widget.attrs.update({'class': 'form-control form-control-sm'})
    supervisor_engineer.widget.attrs.update({'class': 'form-control form-control-sm'})
    contractor_engineer.widget.attrs.update({'class': 'form-control form-control-sm'})
    project_number.widget.attrs.update({'class': 'form-control form-control-sm'})
    exec_documents.widget.attrs.update({'class': 'form-control form-control-sm'})
    supervisor_engineer_decree.widget.attrs.update({'class': 'form-control form-control-sm'})
    contractor_engineer_decree.widget.attrs.update({'class': 'form-control form-control-sm'})

    def update (self, pk):
        changing_obj = get_object_or_404(ObjectActs, pk=pk)
        changing_obj.address = self.cleaned_data['address']
        changing_obj.system_type = self.cleaned_data['system_type']
        changing_obj.designer = self.cleaned_data['designer']
        changing_obj.supervisor_engineer = self.cleaned_data['supervisor_engineer']
        changing_obj.contractor_engineer = self.cleaned_data['contractor_engineer']
        changing_obj.project_number = self.cleaned_data['project_number']
        changing_obj.exec_documents = self.cleaned_data['exec_documents']
        changing_obj.supervisor_engineer_decree = self.cleaned_data['supervisor_engineer_decree']
        changing_obj.contractor_engineer_decree = self.cleaned_data['contractor_engineer_decree']
        changing_obj.save()
        return changing_obj


class HActISForm(forms.Form):
    act_number = forms.CharField(max_length=20, label='Ном. акта')
    act_date = forms.CharField(max_length=50, label='Дата акта')
    presented_work = forms.CharField(max_length=200, label='Предъявл.')
    materials = forms.CharField(max_length=200, label='Материалы')
    permitted_work = forms.CharField(max_length=200, label='Разрешено')
    begin_date = forms.CharField(max_length=50, label='От:')
    end_date = forms.CharField(max_length=50, label='До:')

    act_number.widget.attrs.update({'class': 'form-control form-control-sm'})
    act_date.widget.attrs.update({'class': 'form-control form-control-sm'})
    presented_work.widget.attrs.update({'class': 'form-control form-control-sm'})
    materials.widget.attrs.update({'class': 'form-control form-control-sm'})
    permitted_work.widget.attrs.update({'class': 'form-control form-control-sm'})
    begin_date.widget.attrs.update({'class': 'form-control form-control-sm'})
    end_date.widget.attrs.update({'class': 'form-control form-control-sm'})

    def update(self, pk):
        changing_obj = get_object_or_404(HiddenActIS, pk=pk)
        changing_obj.act_number = self.cleaned_data['act_number']
        changing_obj.act_date = self.cleaned_data['act_date']
        changing_obj.presented_work = self.cleaned_data['presented_work']
        changing_obj.materials = self.cleaned_data['materials']
        changing_obj.permitted_work = self.cleaned_data['permitted_work']
        changing_obj.begin_date = self.cleaned_data['begin_date']
        changing_obj.end_date = self.cleaned_data['end_date']
        changing_obj.save()
        return changing_obj

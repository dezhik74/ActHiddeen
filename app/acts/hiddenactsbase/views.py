from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View

from .forms import ObjectForm, HActISForm
from .models import *
import os

from docxtpl import DocxTemplate
from docx import Document


class ObjectsList(View):
    def get(self, request):
        objs = ObjectActs.objects.order_by("-id")
        return render(request, 'hiddenactsbase/index.html', context={'objects_acts': objs})


class ObjectDetail (View):
    def get(self, request, pk):
        myobj = get_object_or_404(ObjectActs, pk=pk)
        return render(request, 'hiddenactsbase/object_detail.html', context={'myobj': myobj})


def update_obj(obj, cleaned_obj_data, cleaned_act_data):
    obj.address = cleaned_obj_data[0]['address']
    obj.system_type = cleaned_obj_data[0]['system_type']
    obj.designer = cleaned_obj_data[0]['designer']
    obj.contractor = cleaned_obj_data[0]['contractor']
    obj.supervisor_engineer = cleaned_obj_data[0]['supervisor_engineer']
    obj.contractor_engineer = cleaned_obj_data[0]['contractor_engineer']
    obj.project_number = cleaned_obj_data[0]['project_number']
    obj.exec_documents = cleaned_obj_data[0]['exec_documents']
    obj.supervisor_engineer_decree = cleaned_obj_data[0]['supervisor_engineer_decree']
    obj.contractor_engineer_decree = cleaned_obj_data[0]['contractor_engineer_decree']
    i=0
    for act in obj.acts.all():
        act.act_number = cleaned_act_data[i]['act_number']
        act.act_date = cleaned_act_data[i]['act_date']
        act.presented_work = cleaned_act_data[i]['presented_work']
        act.materials = cleaned_act_data[i]['materials']
        act.permitted_work = cleaned_act_data[i]['permitted_work']
        act.begin_date = cleaned_act_data[i]['begin_date']
        act.end_date = cleaned_act_data[i]['end_date']
        i+=1
        act.save()
    obj.save()
    return obj


def create_hidden_act_to_end (request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    myobj.acts.create()
    return redirect(myobj)


def delete_hidden_act (request, pk_obj, pk_act):
    myobj = get_object_or_404(ObjectActs, pk=pk_obj)
    myact = get_object_or_404(myobj.acts.all(),pk=pk_act)
    myact.delete()
    return redirect(myobj)


def copy_object (request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    s = myobj.address
    if len(s) > 93:
        s = s[0:93]
    newobj=ObjectActs.objects.create(
        address = 'Копия: ' + s,
        system_type = myobj.system_type,
        contractor = myobj.contractor,
        designer = myobj.designer,
        supervisor_engineer = myobj.supervisor_engineer,
        contractor_engineer = myobj.contractor_engineer,
        project_number = myobj.project_number,
        exec_documents = myobj.exec_documents,
        supervisor_engineer_decree = myobj.supervisor_engineer_decree,
        contractor_engineer_decree = myobj.contractor_engineer_decree
     )
    for act in myobj.acts.all():
        newobj.acts.create(
            act_number = act.act_number,
            act_date = act.act_date,
            presented_work = act.presented_work,
            materials = act.materials,
            permitted_work = act.permitted_work,
            begin_date = act.begin_date,
            end_date = act.end_date
        )
    return redirect(newobj)


def delete_object(request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    for act in myobj.acts.all():
        act.delete()
    myobj.delete()
    return redirect('objects_list_url')


def doc_append (file1, file2):
    doc1 = Document(file1)
    doc2 = Document(file2)
    doc1.add_page_break()
    for el in doc2.element.body:
        doc1.element.body.append(el)
    doc1.save


def make_hidden_docx(obj, docx_template_name, dynamic_dir_name):
    context = {}
    i=1
    for act in obj.acts.all():
        context['address'] =  obj.address
        context['system_type'] = obj.system_type
        context['contractor'] = obj.contractor
        context['designer'] = obj.designer
        context['supervisor_engineer'] = obj.supervisor_engineer
        context['contractor_engineer'] = obj.contractor_engineer
        context['project_number'] = obj.project_number
        context['exec_documents'] = obj.exec_documents
        context['supervisor_engineer_decree'] = obj.supervisor_engineer_decree
        context['contractor_engineer_decree'] = obj.contractor_engineer_decree
        context['act_number'] = act.act_number
        context['act_date'] = act.act_date
        context['presented_work'] = act.presented_work
        context['materials'] = act.materials
        context['permitted_work'] = act.permitted_work
        context['begin_date'] = act.begin_date
        context['end_date'] = act.end_date
        name=str(i)
        doc = DocxTemplate(docx_template_name)
        doc.render(context)
        doc.save(os.path.join(dynamic_dir_name,name+".docx"))
        i+=1
        context.clear()
    return 'fff'


def make_word_file(request, pk):
    BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(BASE_APP_DIR,'dynamic')
    DOCX_TEMPLATE_DIR =  os.path.join(BASE_APP_DIR,'docx_template')
    docx_template = os.path.join(DOCX_TEMPLATE_DIR,'HiddenActTemtplate2.docx')
    myobj = get_object_or_404(ObjectActs, pk=pk)
    s = make_hidden_docx (myobj, docx_template,dynamic_dir_name)
    return HttpResponse (str(pk)+' '+dynamic_dir_name+s)


def objectedit (request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    ObjectFormSet = formset_factory(form=ObjectForm, extra=0)
    HActISFormSet = formset_factory(form=HActISForm, extra=0)
    initial_obj = [{
        'address': myobj.address,
        'system_type': myobj.system_type,
        'contractor': myobj.contractor,
        'designer': myobj.designer,
        'supervisor_engineer': myobj.supervisor_engineer,
        'contractor_engineer': myobj.contractor_engineer,
        'project_number': myobj.project_number,
        'exec_documents': myobj.exec_documents,
        'supervisor_engineer_decree': myobj.supervisor_engineer_decree,
        'contractor_engineer_decree': myobj.contractor_engineer_decree
    }]
    initial_ha_act = []
    for act in myobj.acts.all():
        initial_ha_act.append({
            'act_number': act.act_number,
            'act_date': act.act_date,
            'presented_work': act.presented_work,
            'materials': act.materials,
            'permitted_work': act.permitted_work,
            'begin_date': act.begin_date,
            'end_date': act.end_date
        })
    if request.method == 'POST':
        object_form_set = ObjectFormSet (request.POST, prefix='object_data')
        ha_form_set = HActISFormSet(request.POST, prefix='hidden_acts')
        if object_form_set.is_valid() and ha_form_set.is_valid():
            new_object_acts = update_obj(myobj, object_form_set.cleaned_data, ha_form_set.cleaned_data)
            return redirect(new_object_acts)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set})
    else:
        object_form_set = ObjectFormSet(prefix='object_data', initial=initial_obj)
        ha_form_set = HActISFormSet(prefix='hidden_acts', initial=initial_ha_act)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set})


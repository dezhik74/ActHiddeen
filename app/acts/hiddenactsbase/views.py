import mimetypes
import os

from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View
from docx import Document
from docxtpl import DocxTemplate

from .forms import ObjectForm, HActISForm
from .models import *


class ObjectsList(View):
    @staticmethod
    def get(request):
        objs = ObjectActs.objects.order_by("-id")
        return render(request, 'hiddenactsbase/index.html', context={'objects_acts': objs})


class ObjectDetail (View):
    @staticmethod
    def get(request, pk):
        my_obj = get_object_or_404(ObjectActs, pk=pk)
        return render(request, 'hiddenactsbase/object_detail.html', context={'myobj': my_obj})


def update_obj(obj, cleaned_obj_data, cleaned_act_data):
    obj.__dict__.update(cleaned_obj_data[0])
    i=0
    for act in obj.acts.all():
        act.__dict__.update(cleaned_act_data[i])
        i += 1
        act.save()
    obj.save()
    return obj


def create_hidden_act_to_end(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    my_obj.acts.create()
    return redirect(my_obj)


def delete_hidden_act(request, pk_obj, pk_act):
    my_obj = get_object_or_404(ObjectActs, pk=pk_obj)
    my_act = get_object_or_404(my_obj.acts.all(), pk=pk_act)
    my_act.delete()
    return redirect(my_obj)


def copy_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    s = my_obj.address
    if len(s) > 93:
        s = s[0:93]
    my_obj.address = 'Копия: ' + s
    new_acts = []
    for act in my_obj.acts.all():
        act.id = None
        act.save()
        new_acts.append(act)
    my_obj.id = None
    my_obj.save()
    for act1 in new_acts:
        my_obj.acts.add(act1)
    return redirect(my_obj)


def delete_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    for act in my_obj.acts.all():
        act.delete()
    my_obj.delete()
    return redirect('objects_list_url')


def doc_append (file1, file2, numb):
    doc1 = Document(file1)
    doc2 = Document(file2)
    for el in doc2.element.body:
        doc1.element.body.append(el)
    #doc1.add_page_break()
    doc1.save(file1)


def make_hidden_docx(obj, docx_template_name, dynamic_dir_name):
    i = 1
    context = {}
    for act in obj.acts.all():
        context = model_to_dict(obj, exclude=['id', 'acts'])
        c2 = model_to_dict(act, exclude=['id'])
        context.update(c2)
        name = str(i)
        doc = DocxTemplate(docx_template_name)
        doc.render(context)
        doc.save(os.path.join(dynamic_dir_name, name + ".docx"))
        i += 1
        context.clear()
    return i-1


def assemble_docx(dynamic_dir_name, num_of_docx):
    result_docx_name = os.path.join(dynamic_dir_name, 'result.docx')
    if os.path.exists(result_docx_name):
        os.remove(result_docx_name)
    if os.path.exists(os.path.join(dynamic_dir_name, '1.docx')):
        os.rename(os.path.join(dynamic_dir_name, '1.docx'), result_docx_name)
    if num_of_docx > 1:
        for i in range(2, num_of_docx+1):
            doc_append(result_docx_name, os.path.join(dynamic_dir_name, str(i)+'.docx'), i)
            os.remove(os.path.join(dynamic_dir_name, str(i) + '.docx'))
    return result_docx_name


def make_word_file(request, pk):
    base_app_dir = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(base_app_dir, 'dynamic')
    if not os.path.exists(dynamic_dir_name):
        os.mkdir(dynamic_dir_name)
    docx_template_dir =  os.path.join(base_app_dir, 'docx_template')
    docx_template = os.path.join(docx_template_dir, 'HiddenActTemtplate2.docx')
    myobj = get_object_or_404(ObjectActs, pk=pk)
    num_of_docx = make_hidden_docx(myobj, docx_template,dynamic_dir_name)
    docx_name = assemble_docx(dynamic_dir_name, num_of_docx)
    fp = open(docx_name, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(docx_name)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(docx_name).st_size)
    response['Content-Disposition'] = "attachment; filename=hidden_acts.docx"

    return response
    # return HttpResponse (str(pk)+' '+dynamic_dir_name+' ' + docx_name)


def object_edit(request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    ObjectFormSet = formset_factory(form=ObjectForm, extra=0)
    HActISFormSet = formset_factory(form=HActISForm, extra=0)
    initial_obj = [model_to_dict(myobj, exclude=['id', 'acts'])]
    initial_ha_act = []
    for act in myobj.acts.all():
        initial_ha_act.append(model_to_dict(act, exclude=['id']))
    if request.method == 'POST':
        object_form_set = ObjectFormSet(request.POST, prefix='object_data')
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


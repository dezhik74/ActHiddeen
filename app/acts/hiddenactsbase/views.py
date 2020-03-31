import mimetypes
import os
from datetime import datetime

from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View
from docx import Document
from docxtpl import DocxTemplate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import ObjectForm, HActISForm, BlowDownActForm, SearchForm
from .models import *


def paged_output(request, objects, template, search_form):
    paginator = Paginator(objects, 15)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)
    return render(request, template,
                  context={'objects_acts': page_objs,
                           'search_form': search_form
                           })


class ObjectsList(View):

    @staticmethod
    def get(request):
        objs = ObjectActs.objects.order_by("-id")
        search_form = SearchForm()
        return paged_output(request, objs, 'hiddenactsbase/index.html', search_form)

    @staticmethod
    def post(request):
        search_form = SearchForm (request.POST)
        if search_form.is_valid():
            objs = ObjectActs.objects.filter(Q(address__icontains=search_form.cleaned_data['search_object'])
                                            | Q(contractor__icontains=search_form.cleaned_data['search_object'])
                                            | Q(system_type__icontains=search_form.cleaned_data['search_object'])).order_by("-id")
            # objs = ObjectActs.objects.filter(address__contains=search_form.cleaned_data['search_object']).order_by("-id")
        else:
            objs = ObjectActs.objects.order_by("-id")
        return paged_output(request, objs, 'hiddenactsbase/index.html', search_form)
        # return  HttpResponse ('rere: ' + objs)

class ObjectDetail (View):
    @staticmethod
    def get(request, pk):
        my_obj = get_object_or_404(ObjectActs, pk=pk)
        return render(request, 'hiddenactsbase/object_detail.html',
                      context={'myobj': my_obj})


def update_obj(obj, cleaned_obj_data, cleaned_act_data, cleaned_blow_down_act_data):
    obj.__dict__.update(cleaned_obj_data[0])
    i = 0
    for act in obj.acts.all():
        act.__dict__.update(cleaned_act_data[i])
        i += 1
        act.save()
    if obj.blow_down_act != None:
        obj.blow_down_act.__dict__.update(cleaned_blow_down_act_data[0])
        obj.blow_down_act.save()
    obj.save()
    return obj


@login_required
def create_hidden_act_to_end(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    my_obj.acts.create()
    return redirect(my_obj)


@login_required
def create_blow_down(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    if my_obj.blow_down_act == None:
        my_obj.blow_down_act = BlowDownAct.objects.create()
        my_obj.save()
    return redirect(my_obj)


@login_required
def delete_hidden_act(request, pk_obj, pk_act):
    my_obj = get_object_or_404(ObjectActs, pk=pk_obj)
    my_act = get_object_or_404(my_obj.acts.all(), pk=pk_act)
    my_act.delete()
    return redirect(my_obj)


@login_required
def copy_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    s = my_obj.address
    if len(s) > 93:
        s = s[0:93]
    my_obj.address = 'Копия: ' + s
    my_obj.create_date = datetime.now().date()
    new_acts = []
    for act in my_obj.acts.all():
        act.id = None
        act.save()
        new_acts.append(act)
    new_b_d_a = None
    if my_obj.blow_down_act != None:
        new_b_d_a = my_obj.blow_down_act
        new_b_d_a.id = None
        new_b_d_a.save()
    my_obj.id = None
    my_obj.save()
    for act1 in new_acts:
        my_obj.acts.add(act1)
    if new_b_d_a != None:
        my_obj.blow_down_act = new_b_d_a
        my_obj.save()
    return redirect(my_obj)


@login_required
def delete_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    for act in my_obj.acts.all():
        act.delete()
    my_obj.delete()
    if my_obj.blow_down_act != None:
        my_obj.blow_down_act.delete()
    return redirect('objects_list_url')


def doc_append(file1, file2, numb):
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
    return i - 1


def assemble_docx(dynamic_dir_name, num_of_docx):
    result_docx_name = os.path.join(dynamic_dir_name, 'result.docx')
    if os.path.exists(result_docx_name):
        os.remove(result_docx_name)
    if os.path.exists(os.path.join(dynamic_dir_name, '1.docx')):
        os.rename(os.path.join(dynamic_dir_name, '1.docx'), result_docx_name)
    if num_of_docx > 1:
        for i in range(2, num_of_docx + 1):
            doc_append(result_docx_name,
                       os.path.join(dynamic_dir_name, str(i) + '.docx'), i)
            os.remove(os.path.join(dynamic_dir_name, str(i) + '.docx'))
    return result_docx_name


def make_word_file(request, pk):
    base_app_dir = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(base_app_dir, 'dynamic')
    if not os.path.exists(dynamic_dir_name):
        os.mkdir(dynamic_dir_name)
    docx_template_dir = os.path.join(base_app_dir, 'docx_template')
    docx_template = os.path.join(docx_template_dir, 'HiddenActTemtplate2.docx')
    myobj = get_object_or_404(ObjectActs, pk=pk)
    num_of_docx = make_hidden_docx(myobj, docx_template, dynamic_dir_name)
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


@login_required
def object_edit(request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    ObjectFormSet = formset_factory(form=ObjectForm, extra=0)
    HActISFormSet = formset_factory(form=HActISForm, extra=0)
    BlowDownActFormSet = formset_factory(form=BlowDownActForm, extra=0)
    initial_obj = [model_to_dict(myobj, exclude=['id', 'acts'])]
    initial_ha_act = []
    initial_blow_down = []
    for act in myobj.acts.all():
        initial_ha_act.append(model_to_dict(act, exclude=['id']))
    if myobj.blow_down_act:
        initial_blow_down.append(model_to_dict(myobj.blow_down_act))
    if request.method == 'POST':
        object_form_set = ObjectFormSet(request.POST, prefix='object_data')
        ha_form_set = HActISFormSet(request.POST, prefix='hidden_acts')
        blow_down_act_form_set = BlowDownActFormSet(request.POST, prefix='blow_down_act')
        if object_form_set.is_valid() and ha_form_set.is_valid() and blow_down_act_form_set.is_valid():
            new_object_acts = update_obj(myobj, object_form_set.cleaned_data,
                                         ha_form_set.cleaned_data, blow_down_act_form_set.cleaned_data)
            return redirect(new_object_acts)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set,
            'blow_down_act_form_set': blow_down_act_form_set})
    else:
        object_form_set = ObjectFormSet(prefix='object_data',
                                        initial=initial_obj)
        ha_form_set = HActISFormSet(prefix='hidden_acts',
                                    initial=initial_ha_act)
        blow_down_act_form_set = BlowDownActFormSet(prefix='blow_down_act',
                                                    initial=initial_blow_down)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set,
            'blow_down_act_form_set': blow_down_act_form_set})


@login_required
def delete_blow_down_act(request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    if myobj.blow_down_act != None:
        b_d_a = myobj.blow_down_act
        b_d_a.delete()
        myobj.blow_down_act = None
    return redirect(myobj)

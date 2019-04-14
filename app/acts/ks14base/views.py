import mimetypes
import os
import re

from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View
from docxtpl import DocxTemplate
from openpyxl import Workbook, load_workbook

from .models import *
from .forms import *
from .create_documents import *

# Create your views here.

def ks14_list(request):
    objs = ObjectCommon.objects.order_by("-id")
    return render(request, 'ks14base/ks14list.html',
                  context={'objects': objs})

def ks14_object_edit_structure(request, pk):
    my_obj = get_object_or_404(ObjectCommon, pk=pk)
    return render(request, 'ks14base/ks14structure.html',locals())

def copy_ks14(request, pk):
    my_obj = get_object_or_404(ObjectCommon, pk=pk)
    my_obj.copy()
    return redirect('ks14_list_url')


def delete_ks14(request, pk):
    my_obj = get_object_or_404(ObjectCommon, pk=pk)
    my_obj.delete_common_obj()
    return redirect('ks14_list_url')


def make_ks14_docx (request, pk, pk2):
    my_obj = get_object_or_404(ObjectCommon, pk=pk)
    my_act = get_object_or_404(ActSpecific, pk=pk2)
    return create_ks14_docx(my_obj, my_act)


def make_ks3_xlsx(request, pk, pk2):
    my_obj=get_object_or_404(Ks14Act, pk=pk)
    my_act = get_object_or_404(ActSpecific, pk=pk2)
    return create_ks3_xlsx (my_obj, my_act)


def make_ks2_xlsx(request, pk, pk2):
    my_obj=get_object_or_404(Ks14Act, pk=pk)
    my_act = get_object_or_404(ActSpecific, pk=pk2)
    return create_ks2_xlsx (my_obj, my_act)


def make_peresort (request, pk, pk2):
    my_obj = get_object_or_404(Ks14Act, pk=pk)
    my_act = get_object_or_404(ActSpecific, pk=pk2)
    return create_peresort (my_obj, my_act)


class KS14_Detail(View):
    @staticmethod
    def get(request, pk):
        my_obj = get_object_or_404(ObjectCommon, pk=pk)
        return render(request, 'ks14base/ks14_detail.html',
                      context={'my_object': my_obj})


def ks14_object_edit(request, pk):
    my_obj = get_object_or_404(ObjectCommon, pk=pk)
    ObjectCommonFormSet = formset_factory(form=ObjectCommonForm, extra=0)
    ActSpecificFormSet = formset_factory(form=ActSpecificForm, extra=0)
    init_data_common_obj = [model_to_dict(my_obj, exclude=['id', 'acts'])]
    init_data_acts = []
    for act in my_obj.acts.all():
        init_data_acts.append(model_to_dict(act, exclude=['id']))
    if request.method == 'POST':
        object_common_form_set = ObjectCommonFormSet(request.POST, prefix ='common_object_data')
        act_specific_form_set = ActSpecificFormSet(request.POST, prefix ='act_data')
        if object_common_form_set.is_valid() and act_specific_form_set.is_valid():
            my_obj.update_object_common (object_common_form_set.cleaned_data, act_specific_form_set.cleaned_data)
            return redirect('ks14_list_url')
        return render(request, 'ks14base/object_edit.html', context = {'my_obj' : my_obj,
                                                                       'object_common_form_set' : object_common_form_set,
                                                                       'act_specific_form_set' : act_specific_form_set})
    else:
        object_common_form_set = ObjectCommonFormSet(prefix='common_object_data', initial=init_data_common_obj)
        act_specific_form_set = ActSpecificFormSet(prefix='act_data', initial=init_data_acts)
        return render(request, 'ks14base/object_edit.html', context = {'my_obj' : my_obj,
                                                                       'object_common_form_set' : object_common_form_set,
                                                                       'act_specific_form_set' : act_specific_form_set})





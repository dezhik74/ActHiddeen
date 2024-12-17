import mimetypes
import os
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from .certificates import compose_cert_file
from .forms import ObjectForm, HActISForm, SearchForm
from .models import ObjectActs, Certificate
from .AssembleFile import AssembleFile


def main_index(request):
    return render(request, 'hiddenactsbase/index_main.html')


def paged_output(request, objects, template, search_form):
    paginator = Paginator(objects, 30)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)
    return render(request, template,
                  context={'objects_acts': page_objs,
                           'search_form': search_form
                           })


class ObjectsList(LoginRequiredMixin, View):
    login_url = ''

    @staticmethod
    def get(request):
        objs = ObjectActs.objects.order_by("-id")
        search_form = SearchForm()
        return paged_output(request, objs, 'hiddenactsbase/index.html', search_form)

    @staticmethod
    def post(request):
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            objs = ObjectActs.objects.filter(Q(address__icontains=search_form.cleaned_data['search_object'])
                                             | Q(contractor__icontains=search_form.cleaned_data['search_object'])
                                             | Q(
                system_type__icontains=search_form.cleaned_data['search_object'])).order_by("-id")
        else:
            objs = ObjectActs.objects.order_by("-id")
        return paged_output(request, objs, 'hiddenactsbase/index.html', search_form)
        # return  HttpResponse ('rere: ' + objs)


class ObjectDetail(LoginRequiredMixin, DetailView):
    login_url = ''
    template_name = 'hiddenactsbase/object_detail.html'
    model = ObjectActs
    context_object_name = 'my_obj'


class ObjectTableView(ObjectDetail):
    template_name = 'hiddenactsbase/object_table.html'


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
        certificates = [cert for cert in act.certificates.all()]
        act.id = None
        act.save()
        for cert in certificates:
            act.certificates.add(cert)
        new_acts.append(act)
    my_obj.id = None
    my_obj.save()
    for act1 in new_acts:
        my_obj.acts.add(act1)
    return redirect(my_obj)


@login_required
def delete_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    for act in my_obj.acts.all():
        act.delete()
    my_obj.delete()
    return redirect('objects_list_url')


def make_word_file(request, pk):
    obj = get_object_or_404(ObjectActs, pk=pk)
    docx_name = AssembleFile(obj, request.user.username)

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


def make_cert_file(request, pk):
    obj = get_object_or_404(ObjectActs, pk=pk)
    buffer = compose_cert_file(obj)
    response = HttpResponse(buffer, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename=certificates.docx'
    # response['Content-Length'] = str(len(buffer))
    return response


@login_required
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
            myobj.update_obj(object_form_set.cleaned_data,
                             ha_form_set.cleaned_data)
            return redirect(myobj)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set,
        })
    else:
        object_form_set = ObjectFormSet(prefix='object_data',
                                        initial=initial_obj)
        ha_form_set = HActISFormSet(prefix='hidden_acts',
                                    initial=initial_ha_act)
        return render(request, 'hiddenactsbase/object_edit.html', context={
            'myobj': myobj,
            'object_form_set': object_form_set,
            'ha_form_set': ha_form_set,
        })


def new_object_edit(request, pk):
    ctx = {"object_id": pk}
    return render(request, 'hiddenactsbase/new_object_edit.html', context=ctx)


def get_object(request, pk):
    my_obj = get_object_or_404(ObjectActs, pk=pk)
    acts = []
    for act in my_obj.acts.all():
        acts.append(model_to_dict(act, exclude=['certificates']))
        acts[-1]['certificates'] = []
        for cert in act.certificates.all():
            acts[-1]['certificates'].append(model_to_dict(cert, exclude=['filename']))
    all_certs = []
    for cert in Certificate.objects.all():
        all_certs.append(model_to_dict(cert, exclude=['filename']))
    result = {
        "my_object": model_to_dict(my_obj, exclude=['acts']),
        "acts": acts,
        "all_certs": all_certs,
    }
    return JsonResponse(result)

from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import View
from .models import *
from .forms import ObjectForm, HActISForm
from django.forms import formset_factory


class ObjectsList (View):
    def get(self,request):
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
    newobj=ObjectActs.objects.create(
        address = myobj.address,
        system_type = myobj.system_type,
        designer = myobj.designer,
        supervisor_engineer = myobj.supervisor_engineer,
        contractor_engineer = myobj.contractor_engineer,
        project_number = myobj.project_number,
        exec_documents = myobj.exec_documents,
        supervisor_engineer_decree = myobj.supervisor_engineer_decree,
        contractor_engineer_decree = myobj.contractor_engineer_decree
     )
    # for act in myobj.acts.all():
    #     newobj.acts.create(
    #         act_number = act.act_number,
    #         act_date = act.act_date,
    #         presented_work = act.presented_work,
    #         materials = act.materials,
    #         permitted_work = act.permitted_work,
    #         begin_date = act.begin_date,
    #         end_date = act.end_date
    #     )
    #return redirect('objects_list_url')
    return redirect(newobj)



def objectedit (request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    ObjectFormSet = formset_factory(form=ObjectForm, extra=0)
    HActISFormSet = formset_factory(form=HActISForm, extra=0)
    initial_obj = [{
        'address': myobj.address,
        'system_type': myobj.system_type,
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


# class ObjectEdit(View):
    # len(oa1.acts.all()) !!! длина списка актов скрытых. Если 0, то их нет !!!
    # ИДЕЯ ДЛЯ соединения двух форм на одной странице
    # ObjectFormSet = formset_factory(ObjectForm)
    # HActISFormSet = formset_factory(HActISForm, extra=6)
    # object_form_set = ObjectFormSet(prefix='objects')
    # hact_is_form_set = HActISFormSet(prefix='hacts')
    # print(object_form_set, hact_is_form_set)


    # def get(self,request,pk):
    #     pass

    # def post(self,request,pk):
    #     pass

    # СТАРАЯ РЕАЛИЗАЦИЯ
    # def get(self, request, pk):
    #     myobj = get_object_or_404(ObjectActs, pk=pk)
    #     ObjectFormSet = formset_factory(ObjectForm, extra=0)
    #     object_form_set = ObjectFormSet (prefix='object_data', initial=[{
    #         'address': myobj.address,
    #         'system_type': myobj.system_type,
    #         'designer': myobj.designer,
    #         'supervisor_engineer': myobj.supervisor_engineer,
    #         'contractor_engineer': myobj.contractor_engineer,
    #         'project_number': myobj.project_number,
    #         'exec_documents': myobj.exec_documents,
    #         'supervisor_engineer_decree': myobj.supervisor_engineer_decree,
    #         'contractor_engineer_decree': myobj.contractor_engineer_decree
    #     }])
    #     # acts_num=len(myobj.acts.all())
    #     initial = []
    #     for act in myobj.acts.all():
    #         initial.append({
    #             'act_number' : act.act_number,
    #             'act_date' : act.act_date,
    #             'presented_work' : act.presented_work,
    #             'materials' : act.materials,
    #             'permitted_work' : act.permitted_work,
    #             'begin_date' : act.begin_date,
    #             'end_date' : act.end_date
    #         })
    #     HActISFormSet = formset_factory(HActISForm, extra=0)
    #     ha_form_set=HActISFormSet(prefix='hidden_acts', initial = initial)
    #     return render(request, 'hiddenactsbase/object_edit.html', context={
    #         'myobj': myobj,
    #         'object_form_set': object_form_set,
    #         'ha_form_set':ha_form_set})
    #     # return HttpResponse(acts_num)
    #
    # def post(self,request,pk):
    #     myobj = get_object_or_404(ObjectActs, pk=pk)
    #     ObjectFormSet = formset_factory(ObjectForm, extra=0)
    #     HActISFormSet = formset_factory(HActISForm, extra=0)
    #     object_form_set = ObjectFormSet (request.POST, prefix='object_data')
    #     ha_form_set = HActISFormSet(request.POST, prefix='hidden_acts')
    #     i1= object_form_set.is_valid()
    #     i2 = ha_form_set.is_valid()
    #     if object_form_set.is_valid() and ha_form_set.is_valid():
    #         print(object_form_set.cleaned_data)
    #         print(ha_form_set.cleaned_data)
    #         new_object_acts = myobj
    #         return redirect(new_object_acts)
    #     return render(request, 'hiddenactsbase/object_edit.html', context={'myobj': myobj, 'form': form})



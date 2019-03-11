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


class ObjectEdit(View):
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
    def get(self, request, pk):
        myobj = get_object_or_404(ObjectActs, pk=pk)
        form=ObjectForm({'address': myobj.address,
                        'system_type': myobj.system_type,
                        'designer': myobj.designer,
                        'supervisor_engineer': myobj.supervisor_engineer,
                        'contractor_engineer': myobj.contractor_engineer,
                        'project_number': myobj.project_number,
                        'exec_documents': myobj.exec_documents,
                        'supervisor_engineer_decree': myobj.supervisor_engineer_decree,
                        'contractor_engineer_decree': myobj.contractor_engineer_decree
        })
        acts_num=len(myobj.acts.all())
        HActISFormSet = formset_factory(HActISForm, extra=acts_num)
        ha_form_set=HActISFormSet(prefix='hidden_acts')
        return render(request, 'hiddenactsbase/object_edit.html', context={'myobj': myobj, 'form': form, 'ha_form_set':ha_form_set})
        # return HttpResponse(acts_num)

    def post(self,request,pk):
        myobj = get_object_or_404(ObjectActs, pk=pk)
        form = ObjectForm(request.POST)
        if form.is_valid():
            new_object_acts = form.update(pk)
            return redirect(new_object_acts)
        return render(request, 'hiddenactsbase/object_edit.html', context={'myobj': myobj, 'form': form})



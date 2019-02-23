from django.shortcuts import render, get_object_or_404
from .models import *
#from django.http import HttpResponse

def acts_list (request):
 #   for act_set in HASet.objects.order_by("id"):
 #       print(HAStandAlone.objects.filter(ha_set=act_set).order_by('id'))
    objs = ObjectActs.objects.order_by("-id")
    return render(request,'hiddenactsbase/index.html',context = {'objects_acts': objs})


def act_detail(request, pk):
    myobj = get_object_or_404(ObjectActs, pk=pk)
    return render(request,'hiddenactsbase/act_detail.html',context = {'myobj': myobj})
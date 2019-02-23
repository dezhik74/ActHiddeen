from django.shortcuts import render
from .models import *
#from django.http import HttpResponse

def act_list (request):
 #   for act_set in HASet.objects.order_by("id"):
 #       print(HAStandAlone.objects.filter(ha_set=act_set).order_by('id'))
    return render (request,'hiddenactsbase/index.html',context = {'objects_acts' : ObjectActs.objects.order_by("-id"),
                                                                    'acts':HiddenActIS.objects.order_by('id')})
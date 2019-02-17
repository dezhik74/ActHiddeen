from django.shortcuts import render
from django.http import HttpResponse

def act_list (request):
    ns = ['2334', 'привет', 'kuku' ]
    return render (request,'hiddenactsbase/index.html',context = {'names' : ns})
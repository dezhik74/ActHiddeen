from django.shortcuts import render, get_object_or_404
from .models import Ks14Act
from django.views.generic import View

# Create your views here.

def ks14_list(request):
    objs = Ks14Act.objects.order_by("-id")
    return render(request, 'ks14base/ks14list.html',
                  context={'objects': objs})

class KS14_Detail(View):
    @staticmethod
    def get(request, pk):
        my_obj = get_object_or_404(Ks14Act, pk=pk)
        return render(request, 'ks14base/ks14_detail.html',
                      context={'my_object': my_obj})


def object_edit(request, pk):
    pass



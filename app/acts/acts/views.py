
from django.shortcuts import HttpResponse, render


def main_index(request):
    #return HttpResponse("asasf dfa adsf df")
    return render(request, 'acts/index.html')
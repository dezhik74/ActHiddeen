from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .gati_render import get_gati_data


class GatiOrderView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        order_list = get_gati_data()
        if order_list:
            return render(request, 'gati/gati_order_list.html', context={'order_list': order_list})
        return HttpResponse('<h2> Произошла ошибка при запросе API сайта gati-onine.ru </h2>')
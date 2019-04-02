from django.shortcuts import render, HttpResponse
from django.views.generic import View
import requests
import re
import csv


class GatiOrderView(View):
    @staticmethod
    def get(request):
        meta_url = 'http://gati-online.ru/opendata/7803032323-DR/meta.csv'
        user_agent_string = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        meta_data = requests.get(meta_url, stream = True, headers = {'user-agent': user_agent_string})
        result = re.search(r'data-\d{4}-\d\d-\d\d-structure-\d{4}-\d\d-\d\d', meta_data.text).group(0)
        csv_url = r'http://gati-online.ru/opendata/7803032323-DR/' + result + '.csv'
        csv_orders = requests.get(csv_url, stream = True, headers = {'user-agent': user_agent_string})
        f_o = open ('www.csv','wb')
        f_o.write(csv_orders.content)
        f_o.close()
        print('----------------------------------')
        print('----------------------------------')
        print (csv_url)
        print('----------------------------------')
        file_obj = open('www.csv','r')
        reader = csv.reader (file_obj)
        for row in reader:
            print('+'.join(row))
        return render(request, 'gati/gati_order_list.html', context = {'list': 123})

import mimetypes
import os
import re

from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View
from docxtpl import DocxTemplate
from openpyxl import Workbook, load_workbook


from .models import Ks14Act


# Create your views here.

def ks14_list(request):
    objs = Ks14Act.objects.order_by("-id")
    return render(request, 'ks14base/ks14list.html',
                  context={'objects': objs})


def copy_ks14(request, pk):
    my_obj = get_object_or_404(Ks14Act, pk=pk)
    s = my_obj.address
    if len(s) > 93:
        s = s[0:93]
    my_obj.address = 'Копия: ' + s
    my_obj.id = None
    my_obj.save()
    return redirect('ks14_list_url')


def delete_ks14(request, pk):
    my_obj = get_object_or_404(Ks14Act, pk=pk)
    my_obj.delete()
    return redirect('ks14_list_url')


def get_file(file_name, file_name_for_download):
    fp = open(file_name, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(file_name)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(file_name).st_size)
    response['Content-Disposition'] = "attachment; filename=" + file_name_for_download
    return response


def make_ks14_docx (request, pk):
    base_app_dir = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(base_app_dir, 'dynamic')
    if not os.path.exists(dynamic_dir_name):
        os.mkdir(dynamic_dir_name)
    docx_template_dir = os.path.join(base_app_dir, 'docx_template')
    docx_template = os.path.join(docx_template_dir, 'KS14ActTemplate.docx')
    my_obj = get_object_or_404(Ks14Act, pk=pk)
    context = model_to_dict(my_obj, exclude=['id'])
    doc = DocxTemplate(docx_template)
    doc.render(context)
    doc.save(os.path.join(dynamic_dir_name, "ks14.docx"))
    return get_file(os.path.join(dynamic_dir_name, "ks14.docx"), 'ks14.docx')


def make_ks3_xlsx(request, pk):
    my_obj=get_object_or_404(Ks14Act, pk=pk)
    base_app_dir = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(base_app_dir, 'dynamic')
    if not os.path.exists(dynamic_dir_name):
        os.mkdir(dynamic_dir_name)
    docx_template_dir = os.path.join(base_app_dir, 'docx_template')
    docx_template = os.path.join(docx_template_dir, 'KS3 Template.xlsx')
    wb = load_workbook(docx_template,read_only=False)
    ws = wb.active
    ws['B11'] = 'Общество с ограниченной ответственностью «' + my_obj.contractor + '»' + my_obj.contractor_address
    ws['J11'] = my_obj.contractor_OKPO
    ws['B13'] = 'Капитальный ремонт ' + my_obj.system_genitive + 'в многоквартирном доме по адресу: ' + my_obj.address
    ws['J16'] = my_obj.contract_number
    s = my_obj.contract_date.split('.')
    ws['J17'] = s[0]
    ws['K17'] = s[1]
    ws['L17'] = s[2][0:4]
    ws['H24'] = my_obj.act_number
    ws['I24'] = re.search(r'^[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]', my_obj.act_date).group(0)
    ws['K24'] = re.search(r'^[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]', my_obj.begin_fact_date).group(0)
    ws['L24'] = re.search(r'^[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]', my_obj.act_date).group(0)
    ws['B29'] = 'Капитальный ремонт ' + my_obj.system_genitive + 'в многоквартирном доме по адресу: ' + my_obj.address
    ws['K34'] = my_obj.summa
    ws['A45'] = 'Инженер отдела строительного контроля №' + my_obj.supervisor_OSK_number
    ws['A46'] = my_obj.supervisor_decree_dative
    ws['K46'] = my_obj.supervisor_delegate
    ws['A49'] = 'Общество с ограниченной ответственностью «' + my_obj.contractor + '»'
    ws['K50'] = my_obj.contractor_delegate
    if my_obj.administration_order:
        ws['A53'] = my_obj.administration_order
    else:
        ws['A53'] = my_obj.owner_delegate_decree
        ws['K53'] = my_obj.owner_delegate
        ws['A54'] = '(должность)'
        ws['G54'] = '(подпись)'
        ws['K54'] = '  (расшифровка подписи)'
    ws['A56'] = 'Уполномоченный  представитель администрации '+ my_obj.district_prepositional + ' района'
    ws['A57'] = my_obj.administration_delegate_position
    ws['A58'] = my_obj.administration_delegate_decree
    ws['K58'] = my_obj.administration_delegate

    wb.save(os.path.join(dynamic_dir_name, 'ks3.xlsx'))
    wb.close()
    return get_file(os.path.join(dynamic_dir_name, 'ks3.xlsx'), 'ks3.xlsx')


class KS14_Detail(View):
    @staticmethod
    def get(request, pk):
        my_obj = get_object_or_404(Ks14Act, pk=pk)
        return render(request, 'ks14base/ks14_detail.html',
                      context={'my_object': my_obj})


def object_edit (request, pk):
    pass



import os

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from docxtpl import DocxTemplate

from config import settings
from water.forms import WaterAssayForm
from water.models import WaterAssay


class WaterAssayListView(generic.ListView):
    model = WaterAssay
    template_name = 'water/waterassay_list.html'
    context_object_name = 'water_assay_list'
    paginate_by = 30
    ordering = ['-conclusion_date', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.query = self.request.GET.get('q', '').strip()

        if self.query:
            queryset = queryset.filter(
                Q(address__icontains=self.query) |
                Q(customer__icontains=self.query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.query
        # Для кнопки сброса — если есть поиск, показываем её
        context['has_search'] = bool(self.query)
        return context


class WaterAssayCreateView(CreateView):
    model = WaterAssay
    form_class = WaterAssayForm
    template_name = 'water/waterassay_form.html'
    success_url = reverse_lazy('water:assay_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый анализ воды'
        context['save_and_continue'] = True  # чтобы шаблон знал, что это создание
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Анализ воды от {self.object.conclusion_date.strftime('%d.%m.%Y')} успешно создан"
        )
        return response

    def get_success_url(self):
        # Если нажата кнопка "Создать и остаться"
        if 'save_and_edit' in self.request.POST:
            return reverse('water:assay_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('water:assay_list')


class WaterAssayUpdateView(UpdateView):
    model = WaterAssay
    form_class = WaterAssayForm
    template_name = 'water/waterassay_form.html'
    context_object_name = 'assay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.conclusion_date:
            formatted_date = self.object.conclusion_date.strftime("%d.%m.%Y")
            context['title'] = f'Редактирование анализа от {formatted_date}'
        else:
            context['title'] = 'Редактирование анализа (дата отсутствует)'
        context['save_and_continue'] = False
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Изменения успешно сохранены")
        return response

    def get_success_url(self):
        if 'save_and_edit' in self.request.POST:
            return reverse('water:assay_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('water:assay_list')


class WaterAssayCopyView(View):
    def post(self, request, pk):
        original = get_object_or_404(WaterAssay, pk=pk)
        
        # Создаём копию
        duplicate = original
        duplicate.pk = None  # важно! сбрасываем pk → будет новый объект
        duplicate.address = f"КОПИЯ - {original.address or ''}".strip()
        duplicate.save()
        
        formatted_date = duplicate.conclusion_date.strftime("%d.%m.%Y")
        messages.success(request, f"Создано копирование анализа от {formatted_date}")
        
        # Переходим сразу в редактирование копии
        return redirect('water:assay_update', pk=duplicate.pk)


class WaterAssayDeleteView(SuccessMessageMixin, DeleteView):
    model = WaterAssay
    success_url = reverse_lazy('water:assay_list')
    template_name = 'water/waterassay_confirm_delete.html'
    success_message = "Анализ от %(conclusion_date)s успешно удалён"

    def get_success_message(self, cleaned_data):
        return self.success_message % {
            'conclusion_date': self.object.conclusion_date.strftime('%d.%m.%Y')
        }


def generate_water_docx(request, pk):
    assay = get_object_or_404(WaterAssay, pk=pk)

    template_path = os.path.join(settings.BASE_DIR, 'water', 'docx_template', 'water_template.docx')

    if not os.path.exists(template_path):
        messages.error(request, "Шаблон water_template.docx не найден в папке docx_template/")
        return redirect('water:assay_list')

    try:
        doc = DocxTemplate(template_path)

        # Контекст для шаблона — всё, что нужно
        context = {
            'conclusion_date': assay.conclusion_date.strftime('%d.%m.%Y') if assay.conclusion_date else '',
            'customer': assay.customer or '',
            'address': assay.address or '',
            'act_number': assay.act_number or '',
            'act_date': assay.act_date.strftime('%d.%m.%Y') if assay.act_date else '',
            'probe_date': assay.probe_date.strftime('%d.%m.%Y') if assay.probe_date else '',
            'hvs_probe_number': assay.hvs_probe_number or '',
            'gvs_probe_number': assay.gvs_probe_number or '',
            'chemistry_number': assay.chemistry_number or '',
            'chemistry_date': assay.chemistry_date.strftime('%d.%m.%Y') if assay.chemistry_date else '',
            'chemistry_order_number': assay.chemistry_order_number or '',
            'chemistry_order_date': assay.chemistry_order_date.strftime('%d.%m.%Y') if assay.chemistry_order_date else '',
            'bio_number': assay.bio_number or '',
            'bio_date': assay.bio_date.strftime('%d.%m.%Y') if assay.bio_date else '',
            'hvs_bio_code': assay.hvs_bio_code or '',
            'gvs_bio_code': assay.gvs_bio_code or '',
            'hvs_bio_referral': assay.hvs_bio_referral or '',
            'gvs_bio_referral': assay.gvs_bio_referral or '',
            'bio_begin_date': assay.bio_begin_date.strftime('%d.%m.%Y') if assay.bio_begin_date else '',
            'bio_end_date': assay.bio_end_date.strftime('%d.%m.%Y') if assay.bio_end_date else '',
            'hvs_ph': assay.hvs_ph or '',
            'hvs_fe': assay.hvs_fe or '',
            'hvs_turb': assay.hvs_turb or '',
            'hvs_chroma': assay.hvs_chroma or '',
            'hvs_rig': assay.hvs_rig or '',
            'hvs_ox': assay.hvs_ox or '',
            'gvs_ph': assay.gvs_ph or '',
            'gvs_fe': assay.gvs_fe or '',
            'gvs_turb': assay.gvs_turb or '',
            'gvs_chroma': assay.gvs_chroma or '',
            'gvs_rig': assay.gvs_rig or '',
            'gvs_ox': assay.gvs_ox or '',
        }

        doc.render(context)

        # Имя файла
        # safe_address = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in assay.address[:30])
        filename = f"water_analysis.docx"

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        doc.save(response)

        return response

    except Exception as e:
        messages.error(request, f"Ошибка при генерации документа: {str(e)}")
        return redirect('water:assay_list')
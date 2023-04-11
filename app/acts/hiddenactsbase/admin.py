import re

from django.contrib import admin
from .models import ObjectActs, HiddenActIS, Certificate


class HiddenActISInline(admin.TabularInline):
    model = ObjectActs.acts.through


@admin.register(HiddenActIS)
class HiddenActISAdmin(admin.ModelAdmin):
    # inlines = [HiddenActISInline]
    search_fields = ('id',)


@admin.register(ObjectActs)
class ObjectActsAdmin(admin.ModelAdmin):
    # TODO Спорное решение - filter_horizontal практически ничего не дает.
    # inlines = [HiddenActISInline]
    # exclude = ('acts', )
    list_display = ('id', 'address', 'system_type')
    filter_horizontal = ('acts',)
    list_display_links = ('address',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'get_filename', 'year')
    list_display_links = ('id', 'description')

    @admin.display(description='Имя файла')
    def get_filename(self, obj):
        reg_exp = r'^(\w|\d)*/'
        return re.sub(reg_exp, '', obj.filename.name)

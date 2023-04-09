from django.contrib import admin
from .models import ObjectActs, HiddenActIS

class HiddenActISInline(admin.TabularInline):
    model = ObjectActs.acts.through


@admin.register(HiddenActIS)
class HiddenActISAdmin(admin.ModelAdmin):
    inlines = [HiddenActISInline]


@admin.register(ObjectActs)
class ObjectActsAdmin(admin.ModelAdmin):
    # TODO Спорное решение - filter_horizontal практически ничего не дает.
    # inlines = [HiddenActISInline]
    # exclude = ('acts', )
    list_display = ('address', 'system_type')
    filter_horizontal = ('acts',)
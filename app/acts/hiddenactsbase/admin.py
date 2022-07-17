from django.contrib import admin
from .models import *


class HiddenActISInline(admin.TabularInline):
    model = ObjectActs.acts.through


@admin.register(HiddenActIS)
class HiddenActISAdmin(admin.ModelAdmin):
    inlines = [HiddenActISInline]


@admin.register(ObjectActs)
class ObjectActsAdmin(admin.ModelAdmin):
    inlines = [HiddenActISInline]
    exclude = ('acts', )
    list_display = ('address', 'system_type')
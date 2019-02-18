from django.contrib import admin
from .models import HASet
from .models import HAStandAlone

# Register your models here.

admin.site.register(HASet)
admin.site.register(HAStandAlone)


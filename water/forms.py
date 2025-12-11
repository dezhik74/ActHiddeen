
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import WaterAssay

class WaterAssayForm(forms.ModelForm):
    class Meta:
        model = WaterAssay
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'


    def clean_conclusion_date(self):
        """Дата заключения обязательна и не может быть в будущем."""
        date = self.cleaned_data.get('conclusion_date')
        if not date:
            raise ValidationError("Дата заключения обязательна.")
        return date


    def clean_customer(self):
        """Дата заключения обязательна и не может быть в будущем."""
        date = self.cleaned_data.get('customer')
        if not date:
            raise ValidationError("Заказчик обязателен.")
        return date


    def clean_address(self):
        """Дата заключения обязательна и не может быть в будущем."""
        date = self.cleaned_data.get('address')
        if not date:
            raise ValidationError("Адрес обязателен.")
        return date

from django import forms
from .models import Car

# Форма для создания и обновления автомобиля
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description']

    # Метод инициализации формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
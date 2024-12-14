from django import forms
from .models import ProductConfiguration

class ProductConfigurationForm(forms.ModelForm):
    class Meta:
        model = ProductConfiguration
        price = forms.DecimalField(max_digits=7, decimal_places=2, required=False)
        fields = [
            'complete_set',
            'mat',
            'shape',
            'color',
            'carpet_color',
            'car_brand',
            'car_model',
            'production_year',
        ]
        widgets = {
            'complete_set': forms.Select(
                choices=ProductConfiguration.COMPLETE_SET_CHOICES,
                attrs={'class': 'form-select'}
            ),
            'mat': forms.Select(
                choices=ProductConfiguration.MAT_CHOICES,
                attrs={'class': 'form-select'}
            ),
            'shape': forms.RadioSelect(
                choices=ProductConfiguration.SHAPE_CHOICES,
                attrs={'class': 'shape-radio'}
            ),
            'color': forms.RadioSelect(
                choices=ProductConfiguration.COLOR_CHOICES,
                attrs={'class': 'color-radio'}
            ),
            'carpet_color': forms.RadioSelect(
                choices=ProductConfiguration.CARPET_CHOICES,
                attrs={'class': 'carpet-color-radio'}
            ),
            'car_brand': forms.Select(
                choices=ProductConfiguration.CAR_BRAND_CHOICES,
                attrs={'class': 'form-select'}
            ),
            'car_model': forms.Select(
                choices=ProductConfiguration.CAR_MODEL_CHOICES,
                attrs={'class': 'form-select'}
            ),
            'production_year': forms.Select(
                choices=ProductConfiguration.PRODUCTION_YEAR_CHOICES,
                attrs={'class': 'form-select'}
            ),
        }
        labels = {
            'complete_set': '1. Wybierz komplet:',
            'mat': '2. Wybierz matę:',
            'shape': '3. Wybierz kształt komórek:',
            'color': 'Kolor obszycia:',
            'carpet_color': 'Kolor dywanika:',
            'car_brand': '4. Dodaj dane o swoim aucie',
            'car_model': 'Model auta:',
            'production_year': 'Rok produkcji:',
            'price': 'Cena:',  # Добавляем метку для поля price
        }
    def save(self, commit=True):
            # Вызываем метод родительского класса для сохранения формы
            product_configuration = super().save(commit=False)
            product_configuration.save()  # Сохраняем объект ProductConfiguration

            # Если поле price заполнено, обновляем соответствующее поле в модели
            if self.cleaned_data['price'] is not None:
                product_configuration.price = self.cleaned_data['price']
                product_configuration.save()

            return product_configuration
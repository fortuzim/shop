from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from configurate.models import ProductConfiguration
from configurate.forms import ProductConfigurationForm
from .forms import ProductConfigurationForm
from .models import ProductConfiguration

# Используем данные о ценах из модели
COMPLETE_SET_PRICES = {
    'Wybierz komplet': 0.00,
    'ETC Zestaw 2D (przód, tył, tunel) - 390 PLN': 390.00,
    'ETC Zestaw przód 2D - 250 PLN': 250.00,
    'ETC Zestaw tył 2D - 200 PLN': 200.00,
    'Nie potrzebuję dywaników tylko matę': 0.00,
}
MAT_PRICES = {
    'Nie potrzebuję maty': 0.00,
    'Mata do bagażnika - 300 PLN': 300.00,
}

def input_view(request):
    if request.method == 'POST':
        form = ProductConfigurationForm(request.POST)
        print("Данные POST:", request.POST)  # Вывод данных POST
        if form.is_valid():
            try:
                print("Валидные данные формы:", form.cleaned_data)  # Проверка данных после валидации
                complete_set = form.cleaned_data['complete_set']
                mat = form.cleaned_data['mat']
                shape = form.cleaned_data['shape']
                color = form.cleaned_data['color']
                carpet_color = form.cleaned_data['carpet_color']
                car_brand = form.cleaned_data['car_brand']
                car_model = form.cleaned_data['car_model']
                production_year = form.cleaned_data['production_year']

                selected_image_url = request.POST.get('selected_image_url')
                
                complete_set_price = COMPLETE_SET_PRICES.get(complete_set, 0)
                mat_price = MAT_PRICES.get(mat, 0)
                total_price = complete_set_price + mat_price  # Общая сумма
                
                product_config = ProductConfiguration(
                    complete_set=complete_set,
                    mat=mat,
                    shape=shape,
                    color=color,
                    carpet_color=carpet_color,
                    car_brand=car_brand,
                    car_model=car_model,
                    production_year=production_year,
                    price=total_price,
                    quantity_available=1
                )
                product_config.save()

                return render(request, 'configurate/result.html', {
                    'product_config': product_config,
                    "total_price": total_price,
                    'image_url': selected_image_url,
                })
            
            except Exception as e:
                return HttpResponse(f"Ошибка: {str(e)}")
        else:
            print("Ошибки формы:", form.errors)  # Отладка ошибок формы
            car_brands = ProductConfiguration.CAR_BRAND_CHOICES
            car_model_choices = ProductConfiguration.CAR_MODEL_CHOICES
            return render(request, 'configurate/dywaniki.html', {
                'form': form,
                'car_brands': car_brands,
                'car_model_choices': car_model_choices,
            })
    else:
        form = ProductConfigurationForm()
        car_brands = ProductConfiguration.CAR_BRAND_CHOICES
        car_model_choices = ProductConfiguration.CAR_MODEL_CHOICES
        return render(request, 'configurate/dywaniki.html', {
            'form': form,
            'car_brands': car_brands,
            'car_model_choices': car_model_choices,
        })


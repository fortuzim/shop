from django.http import HttpResponse
from django.shortcuts import render
from configurate.models import ProductConfiguration
from configurate.forms import ProductConfigurationForm

from configurate.choices import (
    CAR_BRAND_CHOICES,
    CAR_MODEL_CHOICES,
    COMPLETE_SET_PRICES,
    MAT_PRICES,
)


def input_view(request):
    if request.method == "POST":
        form = ProductConfigurationForm(request.POST)
        if form.is_valid():
            try:
                product_config = ProductConfiguration(
                    is_complete_set=form.cleaned_data["is_complete_set"],
                    material=form.cleaned_data["material"],
                    shape=form.cleaned_data["shape"],
                    color=form.cleaned_data["color"],
                    carpet_color=form.cleaned_data["carpet_color"],
                    car_brand=form.cleaned_data["car_brand"],
                    car_model=form.cleaned_data["car_model"],
                    production_year=form.cleaned_data["production_year"],
                    available_quantity=1,
                )

                product_config.save()

                selected_image_url = request.POST.get("selected_image_url")

                return render(
                    request,
                    "configurate/result.html",
                    {
                        "product_config": product_config,
                        "total_price": product_config.price,
                        "image_url": selected_image_url,
                    },
                )

            except Exception as e:
                return HttpResponse(f"Ошибка: {str(e)}")
        else:
            car_brands = CAR_BRAND_CHOICES
            car_model_choices = CAR_MODEL_CHOICES
            return render(
                request,
                "configurate/dywaniki.html",
                {
                    "form": form,
                    "car_brands": car_brands,
                    "car_model_choices": car_model_choices,
                },
            )
    else:
        form = ProductConfigurationForm()
        car_brands = CAR_BRAND_CHOICES
        car_model_choices = CAR_MODEL_CHOICES
        return render(
            request,
            "configurate/dywaniki.html",
            {
                "form": form,
                "car_brands": car_brands,
                "car_model_choices": car_model_choices,
            },
        )

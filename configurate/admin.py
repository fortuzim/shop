from django.contrib import admin
from .models import ProductConfiguration


@admin.register(ProductConfiguration)
class ProductConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "is_complete_set",
        "material",
        "shape",
        "color",
        "car_brand",
        "car_model",
        "production_year",
        "available_quantity",
    )
    search_fields = ("car_brand", "car_model")
    list_filter = (
        "is_complete_set",
        "material",
        "shape",
        "car_brand",
        "car_model",
    )
    ordering = ("-created_at",)

from django.db import models
from configurate.mixins import CustomCharFieldMixin
from django.core.exceptions import ValidationError

# from django.utils.timezone import now
from configurate.choices import (
    COMPLETE_SET_CHOICES,
    MAT_CHOICES,
    SHAPE_CHOICES,
    COLOR_CHOICES,
    CARPET_CHOICES,
    CAR_BRAND_CHOICES,
    CAR_MODEL_CHOICES,
    PRODUCTION_YEAR_CHOICES,
    COMPLETE_SET_PRICES,
    MAT_PRICES,
)


class ProductConfiguration(CustomCharFieldMixin, models.Model):
    is_complete_set = models.CharField(choices=COMPLETE_SET_CHOICES, null=True)
    material = models.CharField(choices=MAT_CHOICES, blank=True)
    shape = models.CharField(
        choices=SHAPE_CHOICES,
    )
    color = models.CharField(
        choices=COLOR_CHOICES,
    )
    carpet_color = models.CharField(
        choices=CARPET_CHOICES,
    )
    car_brand = models.CharField(
        choices=CAR_BRAND_CHOICES,
    )
    car_model = models.CharField(
        choices=CAR_MODEL_CHOICES,
    )
    production_year = models.CharField(
        choices=PRODUCTION_YEAR_CHOICES,
    )
    available_quantity = models.PositiveSmallIntegerField(
        default=0, verbose_name="Количество в наличии"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Цена продажи",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Configuration"
        verbose_name = "Complectation"
        verbose_name_plural = "Complectations"
        ordering = ("-created_at",)

    def get_price(self):
        """
        Method to get price based on selected is_complete_set and material
        """
        complete_set_price = COMPLETE_SET_PRICES.get(self.is_complete_set, 0)
        material_price = MAT_PRICES.get(self.material, 0)
        price = complete_set_price + material_price
        return price

    # def save(self, *args, **kwargs):
    #     """
    #     Override the save method to update price before saving.
    #     """
    #     self.price = self.get_price()
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Override the save method to update price before saving.
        """
        if self.pk:
            orig = ProductConfiguration.get(pk=self.pk)
            if (
                self.is_complete_set != orig.is_complete_set
                or self.material != orig.material
            ):
                self.price = self.get_price()
        else:
            self.price = self.get_price()
        super().save(*args, *kwargs)

    def clean(self):
        """
        Validate the date before saving
        """
        if self.price < 0:
            raise ValidationError("Цена продажи не может быть отрицательной")
        if self.available_quantity < 0:
            raise ValidationError("Количество в наличии не может быть отрицальным")
        # if (
        #     self.car_brand not in CAR_BRAND_CHOICES
        #     or self.car_model not in CAR_MODEL_CHOICES
        # ):
        #     raise ValidationError("Некорректная марка или модель автомобиля")

    def __str__(self):
        return (
            f"Complectation: {self.is_complete_set}, Material: {self.material}, Shape: {self.shape}, "
            f"Color: {self.color}, Brand: {self.car_brand}, Model: {self.car_model}, "
            f"Year: {self.production_year}"
        )


# from django.db import models
# from django.core.exceptions import ValidationError
# from configurate.choices import (
#     COMPLETE_SET_CHOICES,
#     MAT_CHOICES,
#     SHAPE_CHOICES,
#     COLOR_CHOICES,
#     CARPET_CHOICES,
#     CAR_BRAND_CHOICES,
#     CAR_MODEL_CHOICES,
#     PRODUCTION_YEAR_CHOICES,
#     COMPLETE_SET_PRICES,
#     MAT_PRICES,
# )


# class ProductConfiguration(models.Model):
#     complete_set = models.CharField(
#         max_length=100, choices=COMPLETE_SET_CHOICES, blank=False, null=False
#     )
#     mat = models.CharField(max_length=100, choices=MAT_CHOICES, blank=True)
#     shape = models.CharField(max_length=100, choices=SHAPE_CHOICES, blank=True)
#     color = models.CharField(max_length=100, choices=COLOR_CHOICES, blank=True)
#     carpet_color = models.CharField(max_length=100, choices=CARPET_CHOICES, blank=True)
#     car_brand = models.CharField(max_length=100, choices=CAR_BRAND_CHOICES, blank=True)
#     car_model = models.CharField(max_length=100, choices=CAR_MODEL_CHOICES, blank=True)
#     production_year = models.CharField(
#         max_length=21, choices=PRODUCTION_YEAR_CHOICES, blank=True
#     )
#     price = models.DecimalField(
#         max_digits=7, decimal_places=2, default=0.00, verbose_name="Цена"
#     )
#     quantity_available = models.PositiveSmallIntegerField(
#         default=0, verbose_name="Количество в наличии"
#     )
#     sell_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0.00,
#         verbose_name="Цена продажи",
#         editable=False,
#     )

#     class Meta:
#         db_table = "ProductConfiguration"
#         verbose_name = "Комплектация"
#         verbose_name_plural = "Комплектации"
#         ordering = ("id",)

#     def get_price(self):
#         """
#         Метод для получения цены на основе выбранных complete_set и mat.
#         """
#         complete_set_price = COMPLETE_SET_PRICES.get(self.complete_set, 0)
#         mat_price = MAT_PRICES.get(self.mat, 0)
#         total_price = complete_set_price + mat_price
#         return total_price

#     def save(self, *args, **kwargs):
#         """
#         Переопределяем метод save, чтобы обновить sell_price перед сохранением.
#         """
#         self.sell_price = self.get_price()  # Обновляем цену перед сохранением
#         super().save(*args, **kwargs)

#     def clean(self):
#         """
#         Валидируем данные перед сохранением.
#         """
#         if self.price < 0 or self.sell_price < 0:
#             raise ValidationError("Цена и цена продажи не могут быть отрицательными.")
#         if self.quantity_available < 0:
#             raise ValidationError("Количество в наличии не может быть отрицательным.")

#     def __str__(self):
#         return (
#             f"Комплектация: {self.complete_set}, Материал: {self.mat}, Форма: {self.shape}, "
#             f"Цвет: {self.color}, Марка: {self.car_brand}, Модель: {self.car_model}, "
#             f"Год: {self.production_year}"
#         )

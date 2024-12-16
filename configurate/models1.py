from django.db import models
from configurate.mixins import CustomCharFieldMixin
from django.core.exceptions import ValidationError
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
    is_complete_set = models.CharField(
        choices=COMPLETE_SET_CHOICES,
    )
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
        material_price = MAT_PRICES.get(self.mat, 0)
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
        if (
            self.car_brand not in CAR_BRAND_CHOICES
            or self.car_model not in CAR_MODEL_CHOICES
        ):
            raise ValidationError("Некорректная марка или модель автомобиля")

    def __str__(self):
        return (
            f"Complectation: {self.is_complete_set}, Material: {self.mat}, Shape: {self.shape}, "
            f"Color: {self.color}, Brand: {self.car_brand}, Model: {self.car_model}, "
            f"Year: {self.production_year}"
        )

from django.db import models
from configurate.models import ProductConfiguration
from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Товар",
    )
    configuration = models.ForeignKey(
        to=ProductConfiguration,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Конфигурация",
    )
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def products_price(self):
        if self.product:
            return round(self.product.sell_price * self.quantity, 2)
        # Если конфигурация есть, нужно проверить, имеет ли она цену
        elif self.configuration:
            return round(
                self.configuration.get_price() * self.quantity, 2
            )  # Предположим, что у ProductConfiguration есть sell_price
        return 0

    def __str__(self):
        if self.user and self.product:
            return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.product.quantity}"
        elif self.product:
            return f"Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}"
        else:
            return "Корзина не содержит данных о товаре"

    # def __str__(self):
    #     if self.user:
    #         return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'

    #     return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'

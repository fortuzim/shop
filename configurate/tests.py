from django.test import TestCase
from configurate.models import ProductConfiguration


class ProductConfigurationTestCase(TestCase):
    # Указываем, какие фикстуры загрузить
    fixtures = ["shop/fixtures/configurate/productconfiguration.json"]

    def test_product_configuration_count(self):
        """Проверяем, что количество объектов в фикстуре соответствует ожиданиям."""
        self.assertEqual(ProductConfiguration.objects.count(), 2)

    def test_product_configuration_fields(self):
        """Проверяем корректность загруженных данных."""
        product = ProductConfiguration.objects.get(pk=1)
        self.assertEqual(product.is_complete_set, "basic")
        self.assertEqual(product.material, "leather")
        self.assertEqual(product.price, 150.00)

    def test_price_calculation(self):
        """Проверяем правильность расчета цены."""
        product = ProductConfiguration.objects.get(pk=1)
        expected_price = product.get_price()
        self.assertEqual(product.price, expected_price)

    def test_clean_method_validation(self):
        """Проверяем, что валидация работает корректно."""
        product = ProductConfiguration.objects.get(pk=1)
        product.available_quantity = -5  # Устанавливаем некорректное значение
        with self.assertRaises(Exception) as context:
            product.clean()
        self.assertIn(
            "Количество в наличии не может быть отрицательным", str(context.exception)
        )

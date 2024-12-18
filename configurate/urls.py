from django.urls import path

# from django.views.decorators.cache import cache_page

from configurate import views

app_name = "configurate"

urlpatterns = [
    path("configurate/", views.create_product_configuration, name="input_view"),
]

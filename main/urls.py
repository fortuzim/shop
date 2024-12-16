from django.urls import path

# from django.views.decorators.cache import cache_page

from main import views

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path(
        "contact/",
        views.StaticPageView.as_view(),
        {"page_name": "contact"},
        name="contact",
    ),
    path("onas/", views.StaticPageView.as_view(), {"page_name": "onas"}, name="about"),
    path(
        "privacy/",
        views.StaticPageView.as_view(),
        {"page_name": "privacy"},
        name="privacy",
    ),
    path(
        "regulamin/",
        views.StaticPageView.as_view(),
        {"page_name": "regulamin"},
        name="regulamin",
    ),
]

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('about/', cache_page(60)(views.AboutView.as_view()), name='about'),
# ]

from django.urls import path
# from django.views.decorators.cache import cache_page

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('regulamin/', views.regulamin, name='regulamin'),
    path('onas/', views.onas, name='onas'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
]

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('about/', cache_page(60)(views.AboutView.as_view()), name='about'),
# ]
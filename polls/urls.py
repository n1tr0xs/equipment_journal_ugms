from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='Index'),
    path('cartridges/', views.cartridges_list, name='cartridges_list'),
    path('cartridge/<int:cartridge_id>/', views.cartridge_detail, name='cartridge_detail'),
]

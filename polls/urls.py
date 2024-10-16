from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/', views.CartridgeListView.as_view(), name='cartridge_list'),
    path('cartridge/<int:pk>/', views.CartridgeDetailView.as_view(), name='cartridge_detail'),
]

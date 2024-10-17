from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/', views.CartridgeListView.as_view(), name='cartridge-list'),
    path('cartridge/<int:pk>/', views.CartridgeDetailView.as_view(), name='cartridge-detail'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/', views.CartridgeListView.as_view(), name='cartridge-list'),
    path('cartridges/add', views.CartridgeAddView.as_view(), name='add-cartridge'),
    path('cartridges/delete', views.CartridgeBulkDeleteView.as_view(), name='delete-cartridges')
]

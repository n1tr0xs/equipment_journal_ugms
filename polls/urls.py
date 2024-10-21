from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/edit', views.CartridgeEditView.as_view(), name='cartridge-edit'),
    path('cartridges/add', views.CartridgeAddView.as_view(), name='cartridge-add'),
]

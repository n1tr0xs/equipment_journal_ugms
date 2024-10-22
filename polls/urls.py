from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('structure/edit', views.StructureEditView.as_view(), name='structure-edit'),
    path('structure/add', views.StructureAddView.as_view(), name='structure-add'),
    path('post/edit', views.PostEditView.as_view(), name='post-edit'),
    path('post/add', views.PostAddView.as_view(), name='post-add'),
    path('worksite/edit', views.WorksiteEditView.as_view(), name='worksite-edit'),
    path('worksite/add', views.WorksiteAddView.as_view(), name='worksite-add'),
    path('peripheraltype/edit', views.PeripheralTypeEditView.as_view(), name='peripheraltype-edit'),
    path('peripheraltype/add', views.PeripheralTypeAddView.as_view(), name='peripheraltype-add'),
    path('computerconfiguration/edit', views.ComputerConfigurationEditView.as_view(), name='computerconfiguration-edit'),
    path('computerconfiguration/add', views.ComputerConfigurationAddView.as_view(), name='computerconfiguration-add'),
    path('peripheral/edit', views.PeripheralEditView.as_view(), name='peripheral-edit'),
    path('peripheral/add', views.PeripheralAddView.as_view(), name='peripheral-add'),
    path('networkequipment/edit', views.NetworkEquipmentEditView.as_view(), name='networkequipment-edit'),
    path('networkequipment/add', views.NetworkEquipmentAddView.as_view(), name='networkequipment-add'),
    path('computer/edit', views.ComputerEditView.as_view(), name='computer-edit'),
    path('computer/add', views.ComputerAddView.as_view(), name='computer-add'),
    path('monitor/edit', views.MonitorEditView.as_view(), name='monitor-edit'),
    path('monitor/add', views.MonitorAddView.as_view(), name='monitor-add'),
    path('mfp/edit', views.MFPEditView.as_view(), name='mfp-edit'),
    path('mfp/add', views.MFPAddView.as_view(), name='mfp-add'),
    path('ups/edit', views.UPSEditView.as_view(), name='ups-edit'),
    path('ups/add', views.UPSAddView.as_view(), name='ups-add'),
    path('meteounit/edit', views.MeteoUnitEditView.as_view(), name='meteounit-edit'),
    path('meteounit/add', views.MeteoUnitAddView.as_view(), name='meteounit-add'),
    path('server/edit', views.ServerEditView.as_view(), name='server-edit'),
    path('server/add', views.ServerAddView.as_view(), name='server-add'),
    path('cartridge/edit', views.CartridgeEditView.as_view(), name='cartridge-edit'),
    path('cartridge/add', views.CartridgeAddView.as_view(), name='cartridge-add'),
    path('request/edit/', views.RequestEditView.as_view(), name='request-edit'),
    path('request/add', views.RequestAddView.as_view(), name='request-add'),

    path('request/todo', views.RequestToDoView.as_view(), name='request-todo'),
    path('request/create', views.RequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>', views.RequestDetailView.as_view(), name='request-detail')
]

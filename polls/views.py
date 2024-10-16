from django.shortcuts import render
from django.views.generic import DetailView, ListView


from .models import Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request


def index(request):
    return render(request, 'polls/base.html')


class StructureListView(ListView):
    model = Structure
    context_object_name = ''
    template_name = ''


class PostListView(ListView):
    model = Post
    context_object_name = ''
    template_name = ''


class WorksiteListView(ListView):
    model = Worksite
    context_object_name = ''
    template_name = ''


class PeripheralTypeListView(ListView):
    model = PeripheralType
    context_object_name = ''
    template_name = ''


class ComputerConfigurationListView(ListView):
    model = ComputerConfiguration
    context_object_name = ''
    template_name = ''


class PeripheralListView(ListView):
    model = Peripheral
    context_object_name = ''
    template_name = ''


class NetworkEquipmentListView(ListView):
    model = NetworkEquipment
    context_object_name = ''
    template_name = ''


class ComputerListView(ListView):
    model = Computer
    context_object_name = ''
    template_name = ''


class MonitorListView(ListView):
    model = Monitor
    context_object_name = ''
    template_name = ''


class MFPListView(ListView):
    model = MFP
    context_object_name = ''
    template_name = ''


class UPSListView(ListView):
    model = UPS
    context_object_name = ''
    template_name = ''


class MeteoUnitListView(ListView):
    model = MeteoUnit
    context_object_name = ''
    template_name = ''


class ServerListView(ListView):
    model = Server
    context_object_name = ''
    template_name = ''


class CartridgeListView(ListView):
    model = Cartridge
    context_object_name = 'cartridge_list'
    template_name = 'polls/cartridge_list.html'


class RequestListView(ListView):
    model = Request
    context_object_name = ''
    template_name = ''


class StructureDetailView(DetailView):
    model = Structure
    context_object_name = ''
    template_name = ''


class PostDetailView(DetailView):
    model = Post
    context_object_name = ''
    template_name = ''


class WorksiteDetailView(DetailView):
    model = Worksite
    context_object_name = ''
    template_name = ''


class PeripheralTypeDetailView(DetailView):
    model = PeripheralType
    context_object_name = ''
    template_name = ''


class ComputerConfigurationDetailView(DetailView):
    model = ComputerConfiguration
    context_object_name = ''
    template_name = ''


class PeripheralDetailView(DetailView):
    model = Peripheral
    context_object_name = ''
    template_name = ''


class NetworkEquipmentDetailView(DetailView):
    model = NetworkEquipment
    context_object_name = ''
    template_name = ''


class ComputerDetailView(DetailView):
    model = Computer
    context_object_name = ''
    template_name = ''


class MonitorDetailView(DetailView):
    model = Monitor
    context_object_name = ''
    template_name = ''


class MFPDetailView(DetailView):
    model = MFP
    context_object_name = ''
    template_name = ''


class UPSDetailView(DetailView):
    model = UPS
    context_object_name = ''
    template_name = ''


class MeteoUnitDetailView(DetailView):
    model = MeteoUnit
    context_object_name = ''
    template_name = ''


class ServerDetailView(DetailView):
    model = Server
    context_object_name = ''
    template_name = ''


class CartridgeDetailView(DetailView):
    model = Cartridge
    context_object_name = 'cartridge'
    template_name = 'polls/cartridge_detail.html'


class RequestDetailView(DetailView):
    model = Request
    context_object_name = ''
    template_name = ''

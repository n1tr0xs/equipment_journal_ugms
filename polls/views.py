from django.shortcuts import render
from django.views.generic import DetailView, ListView


from .models import Cartridge


def index(request):
    return render(request, 'polls/base.html')


class CartridgeListView(ListView):
    model = Cartridge
    context_object_name = 'cartridge_list'
    template_name = 'polls/cartridge_list.html'
    queryset = Cartridge.objects.order_by('id')


class CartridgeDetailView(DetailView):
    model = Cartridge
    context_object_name = 'cartridge'
    template_name = 'polls/cartridge_detail.html'

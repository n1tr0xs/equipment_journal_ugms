from django.shortcuts import render, get_object_or_404


from .models import Cartridge


def index(request):
    return render(request, 'polls/base.html')


def cartridges_list(request):
    cartridges = Cartridge.objects.order_by('id')
    context = {
        'cartridges_list': cartridges,
    }
    return render(request, 'polls/cartridges.html', context)


def cartridge_detail(request, cartridge_id):
    cartridge = get_object_or_404(Cartridge, pk=cartridge_id)
    return render(request, 'polls/cartridge.html', {'cartridge': cartridge})

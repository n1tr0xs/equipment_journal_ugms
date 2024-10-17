from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import Cartridge
from .forms import CartridgeFormSet


def index(request):
    return render(request, 'polls/base.html')


class CartridgeListView(ListView):
    model = Cartridge
    template_name = 'polls/cartridge_list.html'


class CartridgeAddView(TemplateView):
    template_name = 'polls/add_cartridge.html'

    def get(self, *args, **kwargs):
        formset = CartridgeFormSet(queryset=Cartridge.objects.none())
        return self.render_to_response({'cartridge_formset': formset})

    def post(self, *args, **kwargs):
        formset = CartridgeFormSet(data=self.request.POST)

        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('cartridge-list'))
        return self.render_to_response({'cartridge_formset': formset})

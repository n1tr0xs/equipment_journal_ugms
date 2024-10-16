from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Cartridge
from .forms import CartridgeAddFormSet, CartridgeEditFormSet


def index(request):
    return render(request, 'polls/base.html')


class CartridgeAddView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/add_objects.html'
    heading = 'Добавить картриджы'
    success_url = reverse_lazy('cartridge-list')
    formset_class = CartridgeAddFormSet

    def get(self, *args, **kwargs):
        forms = self.formset_class(queryset=Cartridge.objects.none())
        context = {
            'heading': self.heading,
            'forms': forms,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        forms = self.formset_class(data=self.request.POST)

        if forms.is_valid():
            forms.save()
            return redirect(self.success_url)

        context = {
            'heading': self.heading,
            'forms': forms,
        }
        return self.render_to_response(context)


class CartridgeListView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/edit_objects.html'
    heading = 'Картриджы'
    success_url = reverse_lazy('cartridge-list')
    formset_class = CartridgeEditFormSet

    def get(self, *args, **kwargs):
        context = {
            'heading': self.heading,
            'forms': self.formset_class,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        forms = self.formset_class(data=self.request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(self.success_url)
        context = {
            'heading': self.heading,
            'forms': forms,
        }
        return self.render_to_response(context)


class CartridgeBulkDeleteView(LoginRequiredMixin, TemplateView):
    model = Cartridge
    success_url = reverse_lazy('cartridge-list')

    def get(self, *args, **kwargs):
        return redirect(self.success_url)

    def post(self, *args, **kwargs):
        total_forms = int(self.request.POST.get('form-TOTAL_FORMS', -1))  # get forms count
        for form_id in range(total_forms):
            deletion_flag = self.request.POST.get(f'form-{form_id}-delete', 'off')
            if deletion_flag == 'on':
                object_id = int(self.request.POST.get(f'form-{form_id}-id', -1))  # get object id
                try:
                    self.model.objects.get(id=object_id).delete()  # deleting object from DB
                except self.model.DoesNotExist:
                    continue

        return redirect(self.success_url)

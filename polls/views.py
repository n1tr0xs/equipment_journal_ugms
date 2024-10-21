from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Cartridge, Request
from .forms import CartridgeFormSet

TABLES_HREFS = {
    model._meta.verbose_name_plural: {
        'edit': reverse_lazy(model.__name__.lower() + '-edit'),
        'add': reverse_lazy(model.__name__.lower() + '-add'),
    }
    for model in [Cartridge]
}


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('table-list'))
    return render(request, 'polls/base.html')


class BaseAddView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/add_objects.html'
    heading_prefix = 'Добавить'
    formset_class = None  # set the formset
    success_url = reverse_lazy('')  # set the success url redirect

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_class.extra = 1

    def get(self, *args, **kwargs):
        forms = self.formset_class(queryset=self.formset_class.model.objects.none())
        context = {
            'heading': self.get_heading(),
            'forms': forms,
            'tables': TABLES_HREFS,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        forms = self.formset_class(data=self.request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(self.success_url)
        context = {
            'heading': self.get_heading(),
            'forms': forms,
            'tables': TABLES_HREFS,
        }
        return self.render_to_response(context)

    def get_heading(self):
        return ' '.join((self.heading_prefix, self.formset_class.model._meta.verbose_name_plural))


class BaseEditView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/edit_objects.html'
    heading_prefix = 'Изменить'
    formset_class = None  # set the formset
    success_url = reverse_lazy('')  # set the success url redirect

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_class.extra = 0
        self.model = self.formset_class.model

    def get(self, *args, **kwargs):
        context = {
            'heading': self.get_heading(),
            'forms': self.formset_class,
            'tables': TABLES_HREFS,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.POST.get('DeleteAction', 0):
            return self.delete(*args, **kwargs)

        forms = self.formset_class(data=self.request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(self.success_url)

        context = {
            'heading': self.get_heading(),
            'forms': forms,
            'tables': TABLES_HREFS,
        }
        return self.render_to_response(context)

    def delete(self, *args, **kwargs):
        total_forms = int(self.request.POST.get('form-TOTAL_FORMS', -1))  # get forms count
        for form_id in range(total_forms):
            deletion_flag = self.request.POST.get(f'form-{form_id}-delete', 'off')  # get deletion flag
            if deletion_flag == 'on':
                object_id = int(self.request.POST.get(f'form-{form_id}-id', -1))  # get object id
                try:
                    self.model.objects.get(id=object_id).delete()  # deleting object from DB
                except self.model.DoesNotExist:
                    continue

        return redirect(self.success_url)

    def get_heading(self):
        return ' '.join((self.heading_prefix, self.formset_class.model._meta.verbose_name_plural))


class CartridgeAddView(BaseAddView):
    formset_class = CartridgeFormSet
    success_url = reverse_lazy('cartridge-edit')


class CartridgeEditView(BaseEditView):
    formset_class = CartridgeFormSet
    success_url = reverse_lazy('cartridge-edit')

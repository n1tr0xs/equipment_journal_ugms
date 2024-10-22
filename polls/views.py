from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView

from .models import Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request
from .forms import StructureFormSet, PostFormSet, WorksiteFormSet, PeripheralTypeFormSet, ComputerConfigurationFormSet, PeripheralFormSet, NetworkEquipmentFormSet, ComputerFormSet, MonitorFormSet, MFPFormSet, UPSFormSet, MeteoUnitFormSet, ServerFormSet, CartridgeFormSet, RequestFormSet, RequestToDoFormSet

TABLES_HREFS = {
    model._meta.verbose_name_plural: reverse_lazy(model.__name__.lower() + '-edit')
    for model in [Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request]
}


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('request-todo'))
    return redirect(reverse_lazy('request-create'))


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
            'nav_sidebar_tables': TABLES_HREFS,
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
            'nav_sidebar_tables': TABLES_HREFS,
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

    def get_queryset(self):
        queryset = self.formset_class.model.objects.all()
        return queryset

    def get(self, *args, **kwargs):
        context = {
            'heading': self.get_heading(),
            'forms': self.formset_class(queryset=self.get_queryset()),
            'nav_sidebar_tables': TABLES_HREFS,
            'add_href': reverse_lazy(self.formset_class.model._meta.model._meta.model_name + '-add'),
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
            'nav_sidebar_tables': TABLES_HREFS,
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


class StructureAddView(BaseAddView):
    formset_class = StructureFormSet
    success_url = reverse_lazy('structure-edit')


class StructureEditView(BaseEditView):
    formset_class = StructureFormSet
    success_url = reverse_lazy('structure-edit')


class PostAddView(BaseAddView):
    formset_class = PostFormSet
    success_url = reverse_lazy('post-edit')


class PostEditView(BaseEditView):
    formset_class = PostFormSet
    success_url = reverse_lazy('post-edit')


class WorksiteAddView(BaseAddView):
    formset_class = WorksiteFormSet
    success_url = reverse_lazy('worksite-edit')


class WorksiteEditView(BaseEditView):
    formset_class = WorksiteFormSet
    success_url = reverse_lazy('worksite-edit')


class PeripheralTypeAddView(BaseAddView):
    formset_class = PeripheralTypeFormSet
    success_url = reverse_lazy('peripheraltype-edit')


class PeripheralTypeEditView(BaseEditView):
    formset_class = PeripheralTypeFormSet
    success_url = reverse_lazy('peripheraltype-edit')


class ComputerConfigurationAddView(BaseAddView):
    formset_class = ComputerConfigurationFormSet
    success_url = reverse_lazy('computerconfiguration-edit')


class ComputerConfigurationEditView(BaseEditView):
    formset_class = ComputerConfigurationFormSet
    success_url = reverse_lazy('computerconfiguration-edit')


class PeripheralAddView(BaseAddView):
    formset_class = PeripheralFormSet
    success_url = reverse_lazy('peripheral-edit')


class PeripheralEditView(BaseEditView):
    formset_class = PeripheralFormSet
    success_url = reverse_lazy('peripheral-edit')


class NetworkEquipmentAddView(BaseAddView):
    formset_class = NetworkEquipmentFormSet
    success_url = reverse_lazy('networkequipment-edit')


class NetworkEquipmentEditView(BaseEditView):
    formset_class = NetworkEquipmentFormSet
    success_url = reverse_lazy('networkequipment-edit')


class ComputerAddView(BaseAddView):
    formset_class = ComputerFormSet
    success_url = reverse_lazy('computer-edit')


class ComputerEditView(BaseEditView):
    formset_class = ComputerFormSet
    success_url = reverse_lazy('computer-edit')


class MonitorAddView(BaseAddView):
    formset_class = MonitorFormSet
    success_url = reverse_lazy('monitor-edit')


class MonitorEditView(BaseEditView):
    formset_class = MonitorFormSet
    success_url = reverse_lazy('monitor-edit')


class MFPAddView(BaseAddView):
    formset_class = MFPFormSet
    success_url = reverse_lazy('mfp-edit')


class MFPEditView(BaseEditView):
    formset_class = MFPFormSet
    success_url = reverse_lazy('mfp-edit')


class UPSAddView(BaseAddView):
    formset_class = UPSFormSet
    success_url = reverse_lazy('ups-edit')


class UPSEditView(BaseEditView):
    formset_class = UPSFormSet
    success_url = reverse_lazy('ups-edit')


class MeteoUnitAddView(BaseAddView):
    formset_class = MeteoUnitFormSet
    success_url = reverse_lazy('meteounit-edit')


class MeteoUnitEditView(BaseEditView):
    formset_class = MeteoUnitFormSet
    success_url = reverse_lazy('meteounit-edit')


class ServerAddView(BaseAddView):
    formset_class = ServerFormSet
    success_url = reverse_lazy('server-edit')


class ServerEditView(BaseEditView):
    formset_class = ServerFormSet
    success_url = reverse_lazy('server-edit')


class CartridgeAddView(BaseAddView):
    formset_class = CartridgeFormSet
    success_url = reverse_lazy('cartridge-edit')


class CartridgeEditView(BaseEditView):
    formset_class = CartridgeFormSet
    success_url = reverse_lazy('cartridge-edit')


class RequestAddView(BaseAddView):
    formset_class = RequestFormSet
    success_url = reverse_lazy('request-edit')


class RequestEditView(BaseEditView):
    formset_class = RequestFormSet
    success_url = reverse_lazy('request-edit')


class RequestToDoView(BaseEditView):
    template_name = 'polls/todo_objects.html'
    formset_class = RequestToDoFormSet
    heading_prefix = 'Активные '
    success_url = reverse_lazy('request-edit')

    def get_queryset(self):
        queryset = self.formset_class.model.objects.filter(
            status__in=[Request.RequestStatus.CREATED, Request.RequestStatus.IN_WORK]
        )
        return queryset

    def post(self, *args, **kwargs):
        if self.request.POST.get('DeleteAction', 0):
            return self.delete(*args, **kwargs)
        forms = self.formset_class(data=self.request.POST)
        if forms.is_valid():
            for form in forms:
                obj = form.save(commit=False)
                if 'completed_at' in form.changed_data:
                    obj.status = Request.RequestStatus.COMPLETED
                obj.save()
            forms.save()
            return redirect(self.success_url)

        context = {
            'heading': self.get_heading(),
            'forms': forms,
            'nav_sidebar_tables': TABLES_HREFS,
        }
        return self.render_to_response(context)


class RequestCreateView(CreateView):
    model = Request
    fields = ['description', 'worksite']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['nav_sidebar_tables'] = TABLES_HREFS
        return context


class RequestDetailView(DetailView):
    model = Request

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['nav_sidebar_tables'] = TABLES_HREFS
        return context

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView
from django_filters.views import FilterView

from .models import Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request, RequestStatus, ServiceHistory, TechnicalCondition
from .forms import StructureFormSet, PostFormSet, WorksiteFormSet, PeripheralTypeFormSet, ComputerConfigurationFormSet, PeripheralFormSet, NetworkEquipmentFormSet, ComputerFormSet, MonitorFormSet, MFPFormSet, UPSFormSet, MeteoUnitFormSet, ServerFormSet, CartridgeFormSet, RequestFormSet, RequestToDoFormSet, ServiceHistoryFilter


def get_nav_sidebar_data():
    return {
        'moderation': {
            model._meta.verbose_name_plural: reverse_lazy(f'{model.__name__.lower()}-edit')
            for model in [Structure, Post, Worksite, PeripheralType, ComputerConfiguration, Peripheral, NetworkEquipment, Computer, Monitor, MFP, UPS, MeteoUnit, Server, Cartridge, Request, ]
        },
        'feedback': {
            'Активные запросы': {
                'href': reverse_lazy('request-todo'),
                'counter': len(Request.objects.filter(status__exact=RequestStatus.CREATED)),
            },
            'История обслуживания': {
                'href': reverse_lazy('service-history'),
            }
        },
    }


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('request-todo'))
    return redirect(reverse_lazy('request-create'))


class BaseView(TemplateView):
    template_name = 'polls/forms_in_table.html'
    title_prefix = None
    formset_class = None
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['nav_sidebar_data'] = get_nav_sidebar_data()
        context['title'] = self.get_title()
        return context

    def get_title(self):
        try:
            return ' '.join([self.title_prefix, self.formset_class.model._meta.verbose_name_plural])
        except (TypeError, AttributeError):
            return ''


class BaseAddView(LoginRequiredMixin, BaseView):
    title_prefix = 'Добавить'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_class.extra = 1

    def get(self, *args, **kwargs):
        formset = self.formset_class(queryset=self.formset_class.model.objects.none())
        context = self.get_context_data()
        context['formset'] = formset
        context['add_form_button'] = True
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(self.success_url)

        formset = self.formset_class(data=self.request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(self.success_url)
        context = self.get_context_data()
        context['formset'] = formset
        return self.render_to_response(context)


class BaseEditView(LoginRequiredMixin, BaseView):
    title_prefix = 'Изменить'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_class.extra = 0
        self.model = self.formset_class.model

    def get_queryset(self):
        queryset = self.formset_class.model.objects.all()
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['add_href'] = reverse_lazy(f'{self.model._meta.model._meta.model_name}-add')
        context['deletion_flag'] = True
        context['no_forms_text'] = 'Нет данных'
        return context

    def get(self, *args, **kwargs):
        context = self.get_context_data()
        context['formset'] = self.formset_class(queryset=self.get_queryset())
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(self.success_url)

        if self.request.POST.get('DeleteAction', 0):
            return self.delete(*args, **kwargs)

        formset = self.formset_class(data=self.request.POST)
        if formset.is_valid():
            for form in formset:
                if 'technical_condition' in form.changed_data:
                    new_object = form.save(commit=False)
                    old_object = self.model.objects.get(id=new_object.id)
                    if new_object.technical_condition in [TechnicalCondition.DISABLED, TechnicalCondition.REPAIRING]:
                        if old_object.technical_condition in [TechnicalCondition.IN_WORK, TechnicalCondition.READY_TO_USE]:
                            service = ServiceHistory.objects.create(
                                device_type=new_object.device_type,
                                device_id=new_object.id,
                                description=new_object.disabling_reason,
                            )
                            new_object.last_service = service
                    elif new_object.technical_condition in [TechnicalCondition.IN_WORK, TechnicalCondition.READY_TO_USE]:
                        if old_object.technical_condition in [TechnicalCondition.DISABLED, TechnicalCondition.REPAIRING]:
                            service = ServiceHistory.objects.get(pk=old_object.last_service.id)
                            service.end()
            formset.save()
            return redirect(self.success_url)

        context = super().get_context_data()
        context['formset'] = formset
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

    def get_title(self):
        return ' '.join((self.title_prefix, self.formset_class.model._meta.verbose_name_plural))


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


class RequestEditView(BaseEditView):
    formset_class = RequestFormSet
    success_url = reverse_lazy('request-edit')

    def get_context_data(self):
        context = super().get_context_data()
        context['add_href'] = False
        return context


class RequestToDoView(BaseEditView):
    formset_class = RequestToDoFormSet
    title_prefix = 'Активные '
    success_url = reverse_lazy('request-todo')

    def get_queryset(self):
        queryset = self.formset_class.model.objects.filter(
            status__in=[RequestStatus.CREATED, RequestStatus.IN_WORK]
        )
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['add_href'] = None
        context['deletion_flag'] = False
        context['no_forms_text'] = 'Все запросы выполнены!'
        return context

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(self.success_url)

        if self.request.POST.get('DeleteAction', 0):
            return self.delete(*args, **kwargs)
        formset = self.formset_class(data=self.request.POST)
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                if 'completed_at' in form.changed_data:
                    obj.status = RequestStatus.COMPLETED
                obj.save()
            formset.save()
            return redirect(self.success_url)

        context = self.get_context_data()
        context['formset'] = formset
        return self.render_to_response(context)


class RequestCreateView(CreateView):
    model = Request
    fields = ['description', 'worksite']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['nav_sidebar_data'] = get_nav_sidebar_data
        context['title'] = 'Создать запрос'
        return context


class RequestDetailView(DetailView):
    model = Request

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f'Запрос № {context["object"].id}'
        context['nav_sidebar_data'] = get_nav_sidebar_data
        return context


class ServiceHistoryView(FilterView):
    model = ServiceHistory
    context_object_name = 'service_history'
    filterset_class = ServiceHistoryFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_sidebar_data'] = get_nav_sidebar_data()
        return context

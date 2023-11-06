from django.contrib import admin
from django.contrib import messages
from .admin_permissions import (
    ProspectPermission, CustomerPermission,
    ContractPermission, EventStatusPermission, EventPermission)
from .models import Prospect, Customer, Contract, EventStatus, Event
from datetime import datetime
from django.shortcuts import redirect
from .forms import EventAdminForm


# prospect
@admin.register(Prospect)
class ProspectAdmin(ProspectPermission, admin.ModelAdmin):

    list_display = ['first_name', 'last_name',
                    'email', 'date_created', 'sales_staff']

    # don't show autopopulate date and staff(request user)
    exclude = ['date_created', 'sales_staff']

    # Only show not_converted prospects
    def get_queryset(self, request):
        return Prospect.objects.all().filter(is_converted=False)

    # save model with specific datas(date=now and staff=request.user)
    def save_model(self, request, obj, form, change):
        obj.date_created = datetime.now()
        obj.sales_staff = request.user  # staff user
        super().save_model(request, obj, form, change)

    # actions to do with selected items
    actions = ['convert_to_customer']

    @admin.action(description='Convertir en client')
    def convert_to_customer(self, request, queryset):
        # print("queryset", queryset)
        # check if lead exists in customer
        for lead in queryset:
            customer = Customer.objects.filter(prospect=lead).exists()
            # if not create the customer with required datas
            if not customer:
                customer = Customer(
                    prospect=lead, first_name=lead.first_name,
                    last_name=lead.last_name, email=lead.email,
                    phone=lead.phone, mobile=lead.mobile,
                    picture_url=lead.picture_url,
                    company_name=lead.company_name,
                    sales_staff=request.user)
                # change prospect status to is_converted
                queryset.update(is_converted=True)
                customer.save()


# customer
@admin.register(Customer)
class CustomerAdmin(CustomerPermission, admin.ModelAdmin):
    list_display = ['prospect', 'sales_staff']

    # actions to do
    actions = ['delete_customer']

    @admin.action(description='Supprimer')
    def update_customer(self, request, queryset):
        queryset.delete()


# contract
@admin.register(Contract)
class ContractAdmin(ContractPermission, admin.ModelAdmin):
    list_display = ['customer', 'date_created', 'status', 'amount']
    # filter contracts (signed or not)
    list_filter = ["status"]
    exclude = ['sales_staff']

    # save model with specific datas(date=now and staff=request.user)
    def save_model(self, request, obj, form, change):
        obj.sales_staff = request.user  # staff user
        super().save_model(request, obj, form, change)

    # actions to do
    actions = ['sign_a_contract', 'create_event']

    @admin.action(description='Signer un contrat')
    def sign_a_contract(self, request, queryset):
        for contract in queryset:
            status = contract.status
        if status is not True:
            queryset.update(status=True)
        return status

    @admin.action(description='Créer un événement')
    # redirect to event creation page
    def create_event(self, request, queryset):
        return redirect("/admin/crm/event/add/")


# eventstatus
@admin.register(EventStatus)
class EventStatusAdmin(EventStatusPermission, admin.ModelAdmin):
    list_display = ['status']


# event
@admin.register(Event)
class EventAdmin(EventPermission, admin.ModelAdmin):
    list_filter = ["support_staff"]
    list_display = [
        'support_staff',
        'contract',
        'event_status',
        # 'date_created',
        # 'date_updated',
        'name',
        'address',
        'attendees',
        'event_date_start',
        'event_date_end',
        # 'notes'
        ]

    form = EventAdminForm

    # save model with datas from form(save_model call clean method
    # with validation condition in forms.py)
    def save_model(self, request, obj, form, change):

        obj.support_staff = form.cleaned_data.get('support_staff')
        obj.event_status = form.cleaned_data.get('event_status')
        obj.name = form.cleaned_data.get('name')
        obj.address = form.cleaned_data.get('address')
        obj.attendees = form.cleaned_data.get('attendees')
        obj.event_date_start = form.cleaned_data.get('event_date_start')
        obj.event_date_end = form.cleaned_data.get('event_date_end')
        obj.notes = form.cleaned_data.get('notes')
        obj.contract = form.cleaned_data.get('contract')
        if change:
            existing_event = Event.objects.filter(
                contract=form.cleaned_data.get('contract')).first()
            if existing_event is not None and existing_event.id != obj.id:
                messages.error(request,
                               'Il y a déjà un événement avec ce contrat. '
                               'Veuillez signer un autre contrat pour '
                               'créer un nouvel événement')
            else:
                obj.save()
        else:
            obj.save()

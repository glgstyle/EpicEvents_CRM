from django.db import models
from django.db.models import Q
from django.conf import settings
from authentication.models import Staff
from datetime import datetime
import pytz


class Prospect(models.Model):
    '''A class to represent a prospect.'''
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to=(Q(role=Staff.Roles.SALES) |
                          Q(role=Staff.Roles.MANAGEMENT)),
        on_delete=models.SET_NULL,
        null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    picture_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_converted = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100)

    # return the firstname and lastname instead of prospect.object
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # return the prospect if he's in a list
    def __repr__(self):
        return self.__str__()


class Customer(models.Model):
    '''A class to represent a customer.'''
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    picture_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    company_name = models.CharField(max_length=100)
    prospect = models.OneToOneField(
        Prospect,
        on_delete=models.SET_NULL,
        null=True)
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        # display only sales staff and manager not support
        limit_choices_to=(Q(role=Staff.Roles.SALES) |
                          Q(role=Staff.Roles.MANAGEMENT)),
        on_delete=models.SET_NULL,
        null=True,
        related_name='sales')

    # return the firstname and lastname instead of customer.object
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # return the customer if he's in a list
    def __repr__(self):
        return self.__str__()


class Contract(models.Model):
    '''A class to represent a contract.'''
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to=(Q(role=Staff.Roles.SALES) |
                          Q(role=Staff.Roles.MANAGEMENT)),
        on_delete=models.SET_NULL,
        null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    end_contract_date = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField()

    # return the firstname and lastname instead of customer.object
    def __str__(self):
        return f"{self.id} {self.customer.last_name} {self.amount}"

    # return the contract if he's in a list
    def __repr__(self):
        return self.__str__()


class EventStatus(models.Model):
    '''A class to represent an event status.'''
    status = models.CharField(
        max_length=25)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Event status"
        verbose_name_plural = "Events status"

    # return the id and status instead of eventStatus.object
    def __str__(self):
        return f"{self.id} {self.status}"

    # return the status if he's in a list
    def __repr__(self):
        return self.__str__()


class Event(models.Model):
    '''A class to represent an event.'''
    support_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to={'role': Staff.Roles.SUPPORT},
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='support_contact')
    contract = models.ForeignKey(
        Contract, limit_choices_to={'status': True},
        on_delete=models.CASCADE)
    event_status = models.ForeignKey(
        EventStatus,
        on_delete=models.SET_NULL,
        null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    attendees = models.IntegerField()
    event_date_start = models.DateTimeField()
    event_date_end = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    # return the name and date instead of event.object
    def __str__(self):
        return f"{self.name} {self.event_date_start}"

    # return the event if he's in a list
    def __repr__(self):
        return self.__str__()

    def is_past(self):
        france = pytz.timezone("Europe/Paris")
        local_time = datetime.now()
        time_now = france.localize(local_time)
        return time_now > self.event_date_end

    def sales_staff(self):
        sales_staff = self.contract.sales_staff.id
        print("*********************************sales_staff", sales_staff)
        return sales_staff

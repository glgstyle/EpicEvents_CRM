from django.db import models
from django.conf import settings


class Prospect(models.Model):
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    picture_url = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    company_name = models.CharField(max_length=100)

    # return the firstname and lastname instead of prospect.object
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # return the prospect if he's in a list
    def __repr__(self):
        return self.__str__()


class Customer(models.Model):
    prospect = models.OneToOneField(
        Prospect,
        on_delete=models.SET_NULL,
        null=True)
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sales')
    management_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managers')

    # return the firstname and lastname instead of customer.object
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # return the customer if he's in a list
    def __repr__(self):
        return self.__str__()


class Contract(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    sales_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
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
    STATUS_CHOICES = (
        # first is displayed and second in database
        ('A venir', 'upcoming'),
        ('En cours', 'processing'),
        ('Terminé', 'done'),
        ('Annulé', 'cancelled'),
    )
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    description = models.CharField(max_length=255, null=True)

    # return the id and status instead of eventStatus.object
    def __str__(self):
        return f"{self.id} {self.status}"

    # return the status if he's in a list
    def __repr__(self):
        return self.__str__()


class Event(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE)
    support_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='support_contact')
    management_staff = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='event_managers')
    contract = models.ForeignKey(
        Contract,
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
    notes = models.TextField(null=True)

    # return the name and date instead of event.object
    def __str__(self):
        return f"{self.name} {self.event_date_start}"

    # return the event if he's in a list
    def __repr__(self):
        return self.__str__()

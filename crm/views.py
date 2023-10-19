from crm.models import Customer, Contract, Event
from crm.serializers import (CustomerSerializer, ContractSerializer,
                             EventSerializer)
from crm.permissions import (IsSellerOrReadOnly, IsCustomerAssigned, IsManager,
                             IsSupport)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response


# Customer
class CustomerViewset(ModelViewSet):
    """View for Customer object. """

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Define the Query String usable in url. """
        queryset = Customer.objects.all()
        customer = self.request.GET.get('customer')
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        if customer is not None:
            queryset = queryset.filter(id=customer)
        elif last_name is not None:
            queryset = queryset.filter(last_name=last_name)
        elif email is not None:
            queryset = queryset.filter(email=email)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the customer
        serializer.save(sales_staff=self.request.user)


# Contract
class ContractList(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly
                          | IsAuthenticated & IsCustomerAssigned
                          | IsAuthenticated & IsManager]
    serializer_class = ContractSerializer

    def get_queryset(self):
        """
        This view should return a list of all the contracts
        with possibility to filter them.
        """
        queryset = Contract.objects.all()
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        date_created = self.request.query_params.get('date_created')
        amount = self.request.query_params.get('amount')
        contract_status = self.request.query_params.get('status')
        payment_due = self.request.query_params.get('payment_due')
        # except Exception as ex:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        if last_name is not None:
            queryset = queryset.filter(customer__last_name=last_name)
        elif email is not None:
            queryset = queryset.filter(customer__email=email)
        elif date_created is not None:
            queryset = queryset.filter(date_created__date=date_created)
        elif amount is not None:
            queryset = queryset.filter(amount=amount)
        elif contract_status is not None:
            queryset = queryset.filter(status=contract_status)
        elif payment_due is not None:
            queryset = queryset.filter(payment_due=payment_due)
        return queryset


class CustomerContractViewset(ModelViewSet):
    """View for Customer Contract. """

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly
                          | IsAuthenticated & IsCustomerAssigned
                          | IsAuthenticated & IsManager]
    serializer_class = ContractSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        # find the customer id in contract object
        queryset = Contract.objects.filter(
            customer=self.kwargs['customer__pk'])
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the contract
        serializer.save(sales_staff=self.request.user)


# Event
class EventList(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly
                          | IsAuthenticated & IsCustomerAssigned
                          | IsAuthenticated & IsManager]
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        This view should return a list of all events
        with possibility to filter them.
        """
        queryset = Event.objects.all()
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        start_date = self.request.query_params.get('date')

        if last_name is not None:
            queryset = queryset.filter(contract__customer__last_name=last_name)
        elif email is not None:
            queryset = queryset.filter(contract__customer__email=email)
        elif start_date is not None:
            queryset = queryset.filter(event_date_start__date=start_date)
        return queryset


class EventContractViewset(ModelViewSet):
    """View for Event object. """

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly
                          | IsAuthenticated & IsCustomerAssigned
                          | IsAuthenticated & IsManager
                          | IsAuthenticated & IsSupport]
    serializer_class = EventSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Event.objects.filter(
            contract=self.kwargs['contract__pk'])
        return queryset

    def perform_create(self, serializer):
        """
        Try to get contract, if doesn't exists
        return 404, else return 200 and save the
        contract id when creating the event.
        """
        try:
            contract = Contract.objects.get(
                id=self.kwargs['contract__pk'])
        except Http404:
            return Response(
                "Item does not exist", status.HTTP_200_OK)
        if contract:
            serializer.save(contract_id=contract.id)
        else:
            return Response(
                "Item already exists", status.HTTP_400_BAD_REQUEST)

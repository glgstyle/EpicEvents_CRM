from crm.models import Customer, Contract, Event
from crm.serializers import (CustomerSerializer, ContractSerializer,
                             EventSerializer)
from crm.permissions import (IsSellerOrReadOnly, IsCustomerAssigned, IsManager,
                             IsSupport)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response


class CustomerViewset(ModelViewSet):
    """View for Customer object. """

    permission_classes = [IsAuthenticated & IsSellerOrReadOnly]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Define the Query String usable in url. """
        queryset = Customer.objects.all()
        customer = self.request.GET.get('customer')
        if customer is not None:
            queryset = queryset.filter(id=customer)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the customer
        serializer.save(sales_staff=self.request.user)


class ContractViewset(ModelViewSet):
    """View for Contract object. """

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
    

class EventViewset(ModelViewSet):
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

from rest_framework import serializers
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        ModelSerializer)
from crm.models import Customer, Contract, Event


class CustomerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']

    def validate_title(self, value):
        # check if customer exists
        if Customer.objects.filter(title=value).exists():
            # if error, DRF raise ValidationError
            raise serializers.ValidationError('Customer already exists')
        return value


class ContractSerializer(ModelSerializer):
    # return the customers info from customer object.
    customer_object = CustomerSerializer(
        source='customer', many=False, read_only=True)

    # quand on modifie un contrat on ne doit pas pouvoir modifier le customer
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['sales_staff', 'customer']


class EventSerializer(ModelSerializer):
    # Return the customers info from object customer
    customer_object = CustomerSerializer(
        source='customer', many=False, read_only=True)

    def validate(self, data):
        """
        Check if event already exists with this contract
        by getting contract id from view and raise error
        if true.
        """
        event_exists = Event.objects.filter(
            contract=self.context['view'].kwargs['contract__pk']).exists()
        # raise error if event exists in db but not if we want tu update
        if (event_exists and not self.context['request'].method == 'PUT' and
                not self.context['request'].method == 'PATCH'):
            raise serializers.ValidationError(
                "Ce contrat a déjà un événement associé, "
                "veuillez créer un autre contrat.")
        return data

    class Meta:
        model = Event
        fields = ['id', 'customer_object', 'support_staff', 'event_status',
                  'date_created', 'date_updated', 'name', 'address',
                  'attendees', 'event_date_start', 'event_date_end', 'notes',
                  'contract_id']
        read_only_fields = ['support_staff', 'contract']

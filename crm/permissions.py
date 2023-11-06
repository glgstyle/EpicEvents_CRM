from rest_framework import permissions
from crm.models import Customer, Contract, Event

from django.contrib.auth.backends import BaseBackend
from django.conf import settings

class MagicAdminBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.username == settings.ADMIN_LOGIN

# permissions
# class IsSellerOrReadOnly(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners(seller) of an object
#     to edit it. Assumes the model instance has an `seller` attribute.
#     """
#     def has_permission(self, request, view):
#         return True

#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if (request.user.is_authenticated and request.user.is_active
#                 and request.method in permissions.SAFE_METHODS):
#             return True
#         # Instance must have an attribute named sales_staff`.
#         return obj.sales_staff == request.user


class IsCustomerAssigned(permissions.BasePermission):
    """
    Object-level permission to only allow owners(sellers) of customers
    contracts to edit it. Assumes the model instance has an `seller` attribute.
    """
    def has_permission(self, request, view):
        # Retrieve the contract_id from view
        obj_id = request.resolver_match.kwargs.get('pk')
        model_name = view.get_queryset().model.__name__
        if model_name == "Event":
            try:
                event = Event.objects.get(pk=obj_id)
                contract = event.contract
            # except:
            #     raise ValueError
            except event.DoesNotExist:
                raise ValueError
        elif model_name == "Contract":
            try:
                contract = Contract.objects.get(pk=obj_id)
            # except:
            #     raise ValueError
            except contract.DoesNotExist:
                raise ValueError
        else:
            print("rien de tout ça")

        if contract is not None:
            if (request.user.is_active
                and contract.sales_staff == request.user):
                return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow Managers
    to get access to CRUD actions.
    Assumes the model instance has an `is_manager` attribute
    or method who return it.
    """
    def has_permission(self, request, view=None):
        if (request.user.is_active and request.user.is_manager):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Customer):
            return True
        elif isinstance(obj, Contract):
            return True
        elif isinstance(obj, Event):
            return True
        return self.has_permission(request, view)


# class IsSupport(permissions.BasePermission):
#     """
#     Object-level permission to only allow Managers
#     to get access to CRUD actions.
#     Assumes the model instance has an `is_support` attribute
#     or method who return it.
#     """
#     def has_permission(self, request, view=None):
#         if (request.user.is_active
#             and request.user.is_support):
#             return True
#         return False

#     def has_object_permission(self, request, view, obj):
#         return self.has_permission(request, view)

# Customer
class HasCustomerPermission(permissions.BasePermission):
    """
    Object-level permission to edit customers. Assumes the model instance
    has an `seller` attribute.
    """
    def has_permission(self, request, view=None):
        if request.user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if (request.user.is_active
                and request.method in permissions.SAFE_METHODS):
            return True
        # Instance must have an attribute named 'sales_staff' or 'is_manager'.
        return obj.sales_staff == request.user or request.user.is_manager

# Contract
class HasContractPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners(seller) of an object
    to edit it. Assumes the model instance has an `seller` attribute.
    """
    def has_permission(self, request, view=None):
        obj_id = request.resolver_match.kwargs.get('customer__pk')
        contract = Contract.objects.filter(pk=obj_id).first()
        # print("obj_id", obj_id)
        # if we want to Read the contracts
        if (request.method in permissions.SAFE_METHODS
            and request.user.is_active):
            return True
        # if we want to POST (to create a contract)
        elif request.user.is_active and request.user.is_manager:
            return True
        elif ((request.user.is_seller) and (contract is not None)
              and (contract.customer.sales_staff == request.user)):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if (request.user.is_active
                and request.method in permissions.SAFE_METHODS):
            return True
        # Instance must have an attribute named 'sales_staff' or 'is_manager'.
        return obj.sales_staff == request.user or request.user.is_manager

# Event
class HasEventPermission(permissions.BasePermission):
    """
    Object-level permission to only allow Managers and support
    to get access to CRUD actions.
    Assumes the model instance has an 'is_support' and 'is_manager' attribute
    or method who return it.
    """

    def has_permission(self, request, view):
        # if we want to Read the event
        # Retrieve the contract_id from view
        obj_id = request.resolver_match.kwargs.get('customer__pk')
        contract = Contract.objects.filter(pk=obj_id).first()
        print("obj_id", obj_id)
        # if we want to Read the event
        if (request.method in permissions.SAFE_METHODS
            and request.user.is_active):
            print("cas 0********")
            return True
        # if we want to POST (to create an event)
        elif request.user.is_active and request.user.is_manager:
            print("cas 1********", request.user.is_active, request.user.is_manager, request.user.role)
            return True
        elif ((request.user.is_seller) and (contract is not None)
              and (contract.sales_staff == request.user)):
            print("cas2*********")
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if (request.user.is_active
                and request.method in permissions.SAFE_METHODS):
            return True
        # Instance must have an attribute named 'sales_staff' or 'is_manager'.
        return obj.support_staff == request.user or request.user.is_manager
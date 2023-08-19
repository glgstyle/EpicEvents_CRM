from authentication.models import Staff


class ProspectPermission():
    '''Define all the CRUD permissions about Prospects.'''
    # CRUD permissions
    # Create
    def has_add_permission(self, request, obj=None):
        '''Define the permission to add a prospect.'''
        # if request user is manager or sales
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Read
    def has_views_permission(self, request, obj=None):
        '''Define the permission to view a prospect.'''
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Update
    def has_change_permission(self, request, obj=None):
        '''Define the permission to update a prospect.'''
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Delete
    def has_delete_permission(self, request, obj=None):
        '''Define the permission to delete a prospect.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False


# Customer Permission
class CustomerPermission():
    '''Define all the CRUD permissions about Customers.'''
    # CRUD permissions
    # Create
    def has_add_permission(self, request, obj=None):
        '''Define the permission to add a customer.'''
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Read
    # all staffs can read customers
    def has_views_permission(self, request, obj=None):
        '''Define the permission to view a customer.'''
        if request.user.role in [
            Staff.Roles.MANAGEMENT,
            Staff.Roles.SALES,
                Staff.Roles.SUPPORT]:
            return True
        return False

    # Update
    def has_change_permission(self, request, obj=None):
        '''Define the permission to update a customer.'''
        # if request user is manager
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        # if customer is not None and is assigned to sales_staff
        elif (obj is not None) and (obj.sales_staff == request.user):
            return True

        return False

    # Delete
    def has_delete_permission(self, request, obj=None):
        '''Define the permission to delete a customer.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False


# Contract Permission
class ContractPermission():
    '''Define all the CRUD permissions about Contracts.'''
    # CRUD permissions
    # Create
    def has_add_permission(self, request, obj=None):
        '''Define the permission to add a contract.'''
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Read
    # all staffs can read contracts
    def has_views_permission(self, request, obj=None):
        '''Define the permission to view a contract.'''
        if request.user.role in [
            Staff.Roles.MANAGEMENT,
            Staff.Roles.SALES,
                Staff.Roles.SUPPORT]:
            return True
        return False

    # Update
    def has_change_permission(self, request, obj=None):
        '''Define the permission to update a contract.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False

    # Delete
    def has_delete_permission(self, request, obj=None):
        '''Define the permission to delete a contract.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False


# Event Status Permissions
class EventStatusPermission():
    '''Define all the CRUD permissions about Event status.'''
    # CRUD permissions
    # Create
    def has_add_permission(self, request, obj=None):
        '''Define the permission to add an event status.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False

    # Read
    def has_views_permission(self, request, obj=None):
        '''Define the permission to view an event status.'''
        if request.user.role in [
            Staff.Roles.MANAGEMENT,
            Staff.Roles.SALES,
                Staff.Roles.SUPPORT]:
            return True
        return False

    # Update
    def has_change_permission(self, request, obj=None):
        '''Define the permission to update an event status.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        # if event is not None and is assigned to support_staff
        elif (obj is not None) and (obj.support_staff == request.user):
            return True
        return False

    # Delete
    # don't delete status
    def has_delete_permission(self, request, obj=None):
        '''Define the permission to delete an event status.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False


# Event Permission
class EventPermission():
    '''Define all the CRUD permissions about Events.'''
    # CRUD permissions
    # Create
    def has_add_permission(self, request, obj=None):
        '''Define the permission to add an event.'''
        if request.user.role in [Staff.Roles.MANAGEMENT, Staff.Roles.SALES]:
            return True
        return False

    # Read
    # all staffs can read events
    def has_views_permission(self, request, obj=None):
        '''Define the permission to view an event.'''
        if request.user.role in [
            Staff.Roles.MANAGEMENT,
            Staff.Roles.SALES,
                Staff.Roles.SUPPORT]:
            return True
        return False

    # Update
    def has_change_permission(self, request, obj=None):
        '''Define the permission to update an event.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        # if event is not None and is assigned to support_staff
        elif (obj is not None) and (obj.support_staff == request.user):
            return True

        return False

    # Delete
    def has_delete_permission(self, request, obj=None):
        '''Define the permission to delete an event.'''
        if request.user.role == Staff.Roles.MANAGEMENT:
            return True
        return False

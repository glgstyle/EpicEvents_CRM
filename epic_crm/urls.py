"""
URL configuration for epic_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from crm.views import (CustomerViewset, CustomerContractViewset,
                       EventContractViewset, ContractList, EventList)

# Customer
router = routers.SimpleRouter()
router.register(r'customers', CustomerViewset, basename='customer')

# Contracts
contracts_router = routers.NestedSimpleRouter(
    router, r'customers', lookup='customer')
contracts_router.register(
    r'contracts', CustomerContractViewset, basename='customer-contracts')

# Contracts List
contracts_list_router = routers.SimpleRouter()
contracts_list_router.register(r'contracts', ContractList,
                               basename='contracts')

# Events
events_router = routers.NestedSimpleRouter(
    contracts_router, 'contracts', lookup='contract')
events_router.register(
    'events', EventContractViewset, basename='customer-contracts-events')

# Events List
events_list_router = routers.SimpleRouter()
events_list_router.register(r'events', EventList,
                            basename='events')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"api/", include("authentication.urls")),
    path(r'api/', include(router.urls)),
    path(r'api/', include(contracts_list_router.urls)),
    path(r'api/', include(contracts_router.urls)),
    path(r'api/', include(events_router.urls)),
    path(r'api/', include(events_list_router.urls)),


]

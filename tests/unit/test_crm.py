from unittest import mock
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import serializers


# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()


# test Admin 
@pytest.mark.django_db
def test_create_prospect_and_redirect(client):
    response = client.post('/admin/crm/prospect/add/',
                           data={'first_name': 'Jacky',
                                 'last_name': 'Chan',
                                 'email': 'jackychan@gmail.com',
                                 'phone': '0102030405',
                                 'mobile': '0602030405',
                                 'picture_url': '',
                                 'is_active':'True',
                                 'is_converted': 'False',
                                 'company_name': 'Fedex'})
    assert response['Location'] == "/admin/login/?next=/admin/crm/prospect/add/"
    assert response.status_code == 302




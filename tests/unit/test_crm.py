import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from crm.models import Prospect


# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()



# test Admin 
# Add prospect
@pytest.mark.django_db
def test_create_prospect():
    prospect = Prospect.objects.create(first_name='Jacky',
                                       last_name = 'Chan',
                                       email = 'jackychan@gmail.com',
                                       phone = '0102030405',
                                       mobile = '0602030405',
                                       picture_url = '',
                                       is_active ='True',
                                       is_converted = 'False',
                                       company_name = 'Fedex')
    assert Prospect.objects.filter(email='jackychan@gmail.com').count() == 1
    assert prospect.phone == '0102030405'
    assert prospect.mobile == '0602030405'


@pytest.mark.django_db
def test_create_prospect_should_redirect(client):
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
    assert response['Location'] == (
        "/admin/login/?next=/admin/crm/prospect/add/")
#     # 200 means the form is being re-displayed with errors
    assert response.status_code == 302

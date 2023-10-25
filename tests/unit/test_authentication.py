import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from authentication.models import Staff


# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()
staff = Staff()


@pytest.mark.django_db
def test_staff_create_and_redirect():
    # Staff.objects.create_user('SALES','john','lennon','lennon@thebeatles.com',
    #                           '0102030405','0601020304','','True','True',
    #                           'False','False')
    # assert Staff.objects.count() == 1
    response = client.post('/admin/authentication/staff/add/',
                            data={'email': 'blabla@gmail.com',
                                  'first_name': 'john',
                                  'last_name': 'lennon',
                                  'phone': '0102030405',
                                  'mobile': '0601020304',
                                  'picture_url': '',
                                  'password': '123',
                                  'confirmation':'123',
                                  'role': "sales"})
    assert response.status_code == 302

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(
        'lennon@thebeatles.com', 'john', 'johnpassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.xfail(raises=ValueError)
def test_user_create_without_email_fail():
    with pytest.raises(
        ValueError, match="Users must have an email address") as exc_info:
            raise ValueError("Users must have an email address")
    User.objects.create_user(
        '', 'john', 'johnpassword')
    assert User.objects.count() == 0
    assert str(exc_info.value) == "Users must have an email address"


@pytest.mark.django_db
@pytest.mark.xfail(raises=ValueError)
def test_user_create_without_firstname_fail():
    with pytest.raises(
        ValueError, match="Users must have a firstname") as exc_info:
            raise ValueError("Users must have a firstname")
    User.objects.create_user(
        'lennon@thebeatles.com', '', 'johnpassword')
    assert User.objects.count() == 0
    assert str(exc_info.value) == "Users must have a firstname"


@pytest.mark.django_db
def test_create_user(client):
    response = client.post('/api/signup/', data={'email': 'blabla@gmail.com',
                                                 'password': '123',
                                                 'confirmation':'123'})
    assert response.status_code == 201

@pytest.mark.django_db
@pytest.mark.xfail()
def test_create_user_without_email_should_fail(client):
    response = client.post('/api/signup/', data={'email': '',
                                                 'password': '123',
                                                 'confirmation':'123'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_superuser_create():
    User.objects.create_superuser(
        'lenny', 'lenny@kravitz.com', 'lennypassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_get_admin_page(client):
    response = client.get('/admin/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login():
    response = client.post(
        "/admin/login/?next=/admin/",
        data={"email": "john@gmail.com",
              "password": "smith"})
    assert response.status_code == 200


# test API
# login test with jwt token/refresh (from fixture in conftest)
@pytest.mark.django_db
def test_login_api_page(api_client):
    response = api_client.post('/api/login/',
                           data={'email': 'sales_staff@gmail.com',
                                 'password': '123'})
    assert response.status_code == 200
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from authentication.models import Staff

# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()


@pytest.mark.django_db
def test_staff_create_should_redirect(client):
    path = reverse('admin:authentication_staff_add')
    response = client.post(path=path,
                            data={'email': 'lennon@thebeatles.com',
                                  'first_name': 'john',
                                  'last_name': 'lennon',
                                  'phone': '0102030405',
                                  'mobile': '0601020304',
                                  'picture_url': '',
                                  'password': '123',
                                  'confirmation':'123',
                                  'role': "sales"})
    assert reversed('admin:authentication_staff_change')
#     # 200 means the form is being re-displayed with errors
    assert response.status_code == 302


@pytest.mark.django_db
def test_admin_create_staff(admin_client):
    response = admin_client.post("/api/signup/",
                           data={'email': 'lennon@thebeatles.com',
                                 'last_name': 'lennon',
                                 'phone': '0102030405',
                                 'mobile': '0601020304',
                                 'picture_url': '',
                                 'password': '123',
                                 'confirmation':'123',
                                 'role': "SALES"},
    )
   
    assert response.status_code == 201
    staff = Staff.objects.filter(email='lennon@thebeatles.com').first()
    assert reversed('admin:authentication_staff_change')
    assert (staff is not None) and (staff.role == "SALES")


def test_with_authenticated_client(client, django_user_model):
    email = "user1@gmail.com"
    password = "bar"
    user = django_user_model.objects.create_user(email=email, password=password)
    # Use this:
    client.force_login(user)
    # Or this:
    response = client.get('/admin/authentication/staff/')
    assert ('Sélectionnez l’objet staff à afficher'
            in response.content.decode('UTF8'))


@pytest.mark.django_db
@pytest.mark.xfail(raises=ValueError)
def test_user_create_without_email_fail():
    with pytest.raises(
        ValueError, match="Users must have an email address") as exc_info:
            raise ValueError("Users must have an email address")
    User.objects.create_user(
        email='', password='johnpassword')
    assert User.objects.count() == 0
    assert str(exc_info.value) == "Users must have an email address"


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



# a remettre 
# # test API
# # login test with jwt token/refresh (from fixture in conftest)

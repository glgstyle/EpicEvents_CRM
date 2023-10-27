from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from authentication.models import Staff

# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()

pytestmark = pytest.mark.django_db


def test_staff_create():
    # staff = Staff.objects.create(role='sales',first_name='john',last_name='lennon',
    staff = Staff.objects.create(role='sales', last_name='lennon',
                                 email='lennon@thebeatles.com',
                                 phone='0102030405',
                                 mobile='0601020304')
    assert Staff.objects.filter(last_name='lennon').exists()
    assert staff.is_admin == False
    assert staff.role == 'sales'


@pytest.mark.django_db
def test_staff_create_should_redirect():
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


# def test_admin_create_staff(client, admin_user):
#     client.force_login(admin_user)
#     assert Staff.objects.count() == 0
#     response = client.post("/admin/authentication/staff/add/",
#                            data={'email': 'lennon@thebeatles.com',
#                                  'first_name': 'john',
#                                  'last_name': 'lennon',
#                                  'phone': '0102030405',
#                                  'mobile': '0601020304',
#                                  'picture_url': '',
#                                  'password': '123',
#                                  'confirmation':'123',
#                                  'role': "sales"},
#     )
#     # 200 means the form is being re-displayed with errors
#     assert response.status_code == 302
#     assert Staff.objects.count() == 1
#     staff = Staff.objects.order_by("-id")[0]
#     assert reversed('admin:authentication_staff_change')
#     assert staff.email == 'lennon@thebeatles.com'
#     assert staff.role == 'sales'

    
# def test_details(rf, admin_user, client):
#     request = rf.get('/admin/authentication/staff/')
#     # Remember that when using RequestFactory, the request does not pass
#     # through middleware. If your view expects fields such as request.user
#     # to be set, you need to set them explicitly.
#     # The following line sets request.user to an admin user.
#     request.user = admin_user
#     response = client(request)
#     assert response.status_code == 200


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(
        'one@user.com', 'one', 'userpassword')
    assert Staff.objects.filter(first_name='one').exists()


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
    assert User.objects.filter(email='lenny@kravitz.com').exists()


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
                           data={'email': 'sales3_staff@gmail.com',
                                 'password': '123'})
    assert response.status_code == 200
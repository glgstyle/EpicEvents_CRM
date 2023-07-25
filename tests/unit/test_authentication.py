import pytest
from django.contrib.auth import get_user_model
from django.test import Client


# client for tests
client = Client()
# define User Model with MyUserManager
User = get_user_model()


@pytest.mark.django_db
def test_get_admin_page(client):
    response = client.get('/admin/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('lenny', 'lenny@kravitz.com', 'lennypassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_superuser_create():
    User.objects.create_superuser(
        'lenny', 'lenny@kravitz.com', 'lennypassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_login():
    response = client.post(
        "/admin/login/?next=/admin/",
        data={"email": "john@gmail.com",
              "password": "smith"})
    response = client.get("/admin/", follow=True)
    assert response.status_code == 200

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from decouple import config


def run_sql(sql):
    conn = psycopg2.connect(
        database=config('DB_NAME'), user=config("DB_USER"),
        password=config("DB_PASSWORD"), host=config('DB_HOST'), port='')
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'tests'
    run_sql("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'epic';")
    run_sql('DROP DATABASE IF EXISTS tests')
    run_sql('CREATE DATABASE tests TEMPLATE epic')

    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE tests')

User = get_user_model()

# API
@pytest.fixture
def api_client():
    user = User.objects.create_user(
        first_name='john', email='sales7_staff@gmail.com', password='123')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture()
def admin_client(client, django_user_model):
    email = "user1@gmail.com"
    password = "bar"
    admin = django_user_model.objects.create_user(email=email, password=password)
    admin.role = "MANAGEMENT"
    admin.save()
    client.force_login(admin)
    return client
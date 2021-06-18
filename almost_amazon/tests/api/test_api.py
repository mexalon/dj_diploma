from decimal import Decimal
import pytest
import random
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_201_CREATED),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_product_auth(admin_api_client, user_factory, is_staff, exp_status):
    some_product = {"name": "test_name", "description": "test_description", "price": 1}
    url = reverse("products-list")

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff

    # TODO Почему это не работает???!!!
    # token = Token.objects.create(user=u)
    # admin_api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    admin_api_client.force_authenticate(user=u)
    resp = admin_api_client.post(url, some_product, )
    assert resp.status_code == exp_status


@pytest.mark.django_db
def test_product_create(admin_api_client, user_factory):
    some_product = {"name": "test_name", "description": "test_description", "price": 1}
    url = reverse("products-list")

    u = user_factory(_quantity=1)[0]
    u.is_staff = True

    admin_api_client.force_authenticate(user=u)
    resp = admin_api_client.post(url, some_product, )

    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json.get('name') == some_product.get("name")
    assert resp_json.get('description') == some_product.get("description")
    assert Decimal(resp_json.get('price')) == some_product.get("price")


@pytest.mark.django_db
def test_product_list(client_api_client, product_factory):
    q = 5
    products = product_factory(_quantity=q)
    url = reverse("products-list")
    resp = client_api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == q
    assert {p.id for p in products} == {p.get('id') for p in resp_json}
    assert {p.name for p in products} == {p.get('name') for p in resp_json}
    assert {p.price for p in products} == {Decimal(p.get('price')) for p in resp_json}
    assert {p.description for p in products} == {p.get('description') for p in resp_json}


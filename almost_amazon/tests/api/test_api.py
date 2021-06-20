import random
from decimal import Decimal

import pytest
from api.serializers import UserSerializer, PositionSerializer
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, \
    HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT, \
    HTTP_403_FORBIDDEN


# ------------- Product tests ------------------


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_201_CREATED),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_product_create(api_client, user_factory, is_staff, exp_status):
    """Тест созданя продукта """
    some_product = {"name": "test_name", "description": "test_description", "price": 1}
    url = reverse("products-list")

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.post(url, some_product, )

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert resp_json.get('name') == some_product.get("name")
        assert resp_json.get('description') == some_product.get("description")
        assert Decimal(resp_json.get('price')) == some_product.get("price")


@pytest.mark.django_db
def test_product_list(api_client, product_factory):
    """Тест листинг продуктов"""
    q = 5
    products = product_factory(_quantity=q)
    url = reverse("products-list")
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == q
    assert {p.id for p in products} == {p.get('id') for p in resp_json}
    assert {p.name for p in products} == {p.get('name') for p in resp_json}
    assert {p.price for p in products} == {Decimal(p.get('price')) for p in resp_json}
    assert {p.description for p in products} == {p.get('description') for p in resp_json}


@pytest.mark.django_db
def test_product_retrieve(api_client, product_factory):
    """Тест извлечения продукта"""
    q = 5
    products = product_factory(_quantity=q)
    p = random.choice(products)
    url = reverse("products-detail", args=[p.id])
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert p.id == resp_json.get('id')
    assert p.name == resp_json.get('name')
    assert p.price == Decimal(resp_json.get('price'))
    assert p.description == resp_json.get('description')


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_product_patch(api_client, product_factory, user_factory, is_staff, exp_status):
    """Тест изменения продукта"""
    q = 5
    products = product_factory(_quantity=q)
    some_product = {"name": "test_name", "description": "test_description", "price": 1}
    p = random.choice(products)
    url = reverse("products-detail", args=[p.id])
    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.patch(url, some_product)

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert p.id == resp_json.get('id')
        assert some_product.get('name') == resp_json.get('name')
        assert some_product.get('price') == Decimal(resp_json.get('price'))
        assert some_product.get('description') == resp_json.get('description')


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_204_NO_CONTENT),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_product_delete(api_client, product_factory, user_factory, is_staff, exp_status):
    """Тест удаления продукта"""
    q = 5
    products = product_factory(_quantity=q)
    p = random.choice(products)
    url = reverse("products-detail", args=[p.id])
    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.delete(url)

    assert resp.status_code == exp_status

    # ------------- Order tests ------------------


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_orders_create(api_client, product_factory, user_factory, is_staff, exp_status):
    """Тест созданя заказа"""
    q = 5
    products = product_factory(_quantity=q)
    order_data = {"positions": [{"product_id": p.id, "amount": random.choice([1, 2, 3])} for p in products]}
    users = user_factory(_quantity=2)
    u = users[0]
    a = users[1]
    a.is_staff = is_staff
    api_client.force_authenticate(user=u)
    url = reverse("orders-list")
    resp = api_client.post(url, data=order_data, format='json')

    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    order_id = resp_json.get("id")
    assert resp_json.get("positions") == order_data.get("positions")

    api_client.force_authenticate(user=a)
    url = reverse("orders-detail", args=[order_id])
    resp = api_client.get(url)
    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert resp_json.get("positions") == order_data.get("positions")


@pytest.mark.django_db
def test_orders_list(api_client, order_factory, user_factory):
    """Тест листинг заказов"""
    q = 5
    orders = order_factory(_quantity=q)
    url = reverse("orders-list")

    a = user_factory(_quantity=1)[0]
    a.is_staff = True
    api_client.force_authenticate(user=a)
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == q


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_orders_retrieve(api_client, order_factory, user_factory, is_staff, exp_status):
    """Тест извлечения заказа"""
    q = 5
    orders = order_factory(_quantity=q)
    o = random.choice(orders)
    url = reverse("orders-detail", args=[o.id])
    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.get(url)

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert o.id == resp_json.get('id')

        s = UserSerializer(o.creator)
        assert s.data == resp_json.get('creator')
        assert o.total == Decimal(resp_json.get('total'))

        pp = [PositionSerializer(p).data for p in o.positions.all()]
        assert pp == resp_json.get('positions')


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_orders_patch(api_client, order_factory, user_factory, is_staff, exp_status):
    """Тест изменения заказа"""
    q = 5
    orders = order_factory(_quantity=q)
    o = random.choice(orders)
    url = reverse("orders-detail", args=[o.id])
    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.patch(url, {"status": "DONE"})

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert o.id == resp_json.get('id')
        assert resp_json.get('status') == 'DONE'


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_204_NO_CONTENT),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_orders_delete(api_client, order_factory, user_factory, is_staff, exp_status):
    """Тест удаления заказа"""
    q = 5
    orders = order_factory(_quantity=q)
    o = random.choice(orders)
    url = reverse("orders-detail", args=[o.id])
    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.delete(url)

    assert resp.status_code == exp_status


# ------------- Review tests ------------------
@pytest.mark.django_db
def test_reviews_create(api_client, user_factory, product_factory):
    """Тест создания отзыва"""
    p = product_factory(_quantity=1)[0]
    r = {"product_id": p.id, "text": "тестовый обзор от клиента", "stars": 4}
    u = user_factory(_quantity=1)[0]
    api_client.force_authenticate(user=u)
    url = reverse("product_reviews-list")
    resp = api_client.post(url, r)
    resp_json = resp.json()

    assert resp.status_code == HTTP_201_CREATED

    s = UserSerializer(u)
    assert s.data == resp_json.get('creator')
    assert r.get("text") == resp_json.get('text')
    assert r.get("product_id") == resp_json.get('product_id')


@pytest.mark.django_db
def test_review_list(api_client, review_factory, user_factory):
    """Тест листинг отзывов"""
    q = 5
    r = review_factory(_quantity=q)
    url = reverse("product_reviews-list")
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == q


@pytest.mark.django_db
def test_reviews_retrieve(api_client, review_factory):
    """Тест извлечения отзыва"""
    q = 5
    reviews = review_factory(_quantity=q)
    r = random.choice(reviews)
    url = reverse("product_reviews-detail", args=[r.id])
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert r.id == resp_json.get('id')

    s = UserSerializer(r.creator)
    assert s.data == resp_json.get('creator')
    assert r.text == resp_json.get('text')
    assert r.product_id.id == resp_json.get('product_id')


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_reviews_patch(api_client, review_factory, user_factory, is_staff, exp_status):
    """Тест изменения отзыва"""
    q = 5
    reviews = review_factory(_quantity=q)
    r = random.choice(reviews)
    url = reverse("product_reviews-detail", args=[r.id])

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.patch(url, {"text": "new text"})

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert r.id == resp_json.get('id')
        assert resp_json.get('text') == 'new text'


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_204_NO_CONTENT),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_reviews_delete(api_client, review_factory, user_factory, is_staff, exp_status):
    """Тест удааления отзыва"""
    q = 5
    reviews = review_factory(_quantity=q)
    r = random.choice(reviews)
    url = reverse("product_reviews-detail", args=[r.id])

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.delete(url)

    assert resp.status_code == exp_status


# ------------- Collections tests ------------------

@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_201_CREATED),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_collection_create(api_client, user_factory, product_factory, is_staff, exp_status):
    """Тест создания коллекции"""
    pp = product_factory(_quantity=2)
    ids = [p.id for p in pp]
    c = {"title": "тестовая подборка", "text": "описание тестовой подборки", "collection_items": ids}
    u = user_factory(_quantity=1)[0]
    api_client.force_authenticate(user=u)
    u.is_staff = is_staff
    url = reverse("product_collections-list")
    resp = api_client.post(url, c)
    resp_json = resp.json()

    assert resp.status_code == exp_status
    if is_staff:
        assert c.get("title") == resp_json.get("title")
        assert c.get("text") == resp_json.get("text")
        assert ids == resp_json.get("collection_items")


@pytest.mark.django_db
def test_collection_list(api_client, collection_factory, user_factory):
    """Тест листинг коллекции"""
    q = 5
    cc = collection_factory(_quantity=q)
    url = reverse("product_collections-list")
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == q


@pytest.mark.django_db
def test_collection_retrieve(api_client, collection_factory):
    """Тест извлечения коллекции"""
    q = 5
    cc = collection_factory(_quantity=q)
    r = random.choice(cc)
    url = reverse("product_collections-detail", args=[r.id])
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert r.id == resp_json.get('id')
    assert r.title == resp_json.get("title")
    assert r.text == resp_json.get("text")
    ids = [p.id for p in r.collection_items.all()]
    assert ids == resp_json.get("collection_items")


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_200_OK),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_collection_patch(api_client, collection_factory, user_factory, is_staff, exp_status):
    """Тест изменения коллекции"""
    q = 5
    cc = collection_factory(_quantity=q)
    r = random.choice(cc)
    url = reverse("product_collections-detail", args=[r.id])

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.patch(url, {"text": "new text"})

    assert resp.status_code == exp_status
    if is_staff:
        resp_json = resp.json()
        assert r.id == resp_json.get('id')
        assert resp_json.get('text') == 'new text'


@pytest.mark.parametrize(["is_staff", "exp_status"],
                         (
                                 (True, HTTP_204_NO_CONTENT),
                                 (False, HTTP_403_FORBIDDEN)
                         )
                         )
@pytest.mark.django_db
def test_collection_delete(api_client, collection_factory, user_factory, is_staff, exp_status):
    """Тест удааления коллекции"""
    q = 5
    cc = collection_factory(_quantity=q)
    r = random.choice(cc)
    url = reverse("product_collections-detail", args=[r.id])

    u = user_factory(_quantity=1)[0]
    u.is_staff = is_staff
    api_client.force_authenticate(user=u)
    resp = api_client.delete(url)

    assert resp.status_code == exp_status

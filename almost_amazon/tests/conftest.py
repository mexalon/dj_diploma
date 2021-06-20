import pytest
from django.conf import settings


from rest_framework.test import APIClient, force_authenticate
from model_bakery import baker


@pytest.fixture
def api_client():
    c = APIClient()
    return c

@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)

    return factory

@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return baker.make('User', **kwargs)

    return factory

@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)

    return factory

@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make('ProductReview', **kwargs)

    return factory

@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make('ProductCollection', **kwargs)

    return factory
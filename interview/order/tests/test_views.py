import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime, timedelta

from interview.order.models import Order

@pytest.mark.django_db
class TestOrderListByDateView:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_order(self):
        def make_order(**kwargs):
            return Order.objects.create(**kwargs)
        return make_order

    def test_list_orders_within_date_range(self, api_client, create_order):
        date1 = datetime.now() - timedelta(days=10)
        date2 = datetime.now() - timedelta(days=5)
        date3 = datetime.now() - timedelta(days=1)

        create_order(name='Order1', created_at=date1)
        create_order(name='Order2', created_at=date2)
        create_order(name='Order3', created_at=date3)

        url = reverse('order-list-by-date')

        response = api_client.get(url, {'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), 'embargo_date': datetime.now().strftime('%Y-%m-%d')})
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2  

        response = api_client.get(url, {'start_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'), 'embargo_date': datetime.now().strftime('%Y-%m-%d')})
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3  

        response = api_client.get(url, {'start_date': 'invalid-date', 'embargo_date': 'invalid-date'})
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data
        assert data['detail'] == 'Invalid date format. Use YYYY-MM-DD.'

    def test_list_orders_with_no_date_range(self, api_client, create_order):
        create_order(name='Order1', created_at=datetime.now() - timedelta(days=10))
        create_order(name='Order2', created_at=datetime.now() - timedelta(days=5))
        create_order(name='Order3', created_at=datetime.now() - timedelta(days=1))

        url = reverse('order-list-by-date')

        response = api_client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3  

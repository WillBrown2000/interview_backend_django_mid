import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from interview.order.models import Order

@pytest.mark.django_db
class TestDeactivateOrderView:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_order(self):
        def make_order(**kwargs):
            return Order.objects.create(**kwargs)
        return make_order

    def test_deactivate_order_success(self, api_client, create_order):
        order = create_order(name='Test Order', is_active=True)
        
        url = reverse('deactivate-order', args=[order.id])
        
        response = api_client.patch(url)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['id'] == order.id
        assert data['is_active'] is False
        
        order.refresh_from_db()
        assert order.is_active is False

    def test_deactivate_order_not_found(self, api_client):
        url = reverse('deactivate-order', args=[999])
        
        response = api_client.patch(url)
        
        assert response.status_code == 404
        data = response.json()
        
        assert 'error' in data
        assert data['error'] == 'Order not found'

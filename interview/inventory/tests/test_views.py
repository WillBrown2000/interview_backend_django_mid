import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime, timedelta

from interview.inventory.models import Inventory
from interview.inventory.serializers import InventorySerializer

@pytest.mark.django_db
class TestInventoryListCreateView:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_inventory(self):
        def make_inventory(**kwargs):
            return Inventory.objects.create(**kwargs)
        return make_inventory

    def test_inventory_list_created_after_date(self, api_client, create_inventory):
        date1 = datetime.now() - timedelta(days=10)
        date2 = datetime.now() - timedelta(days=5)
        date3 = datetime.now() - timedelta(days=1)

        create_inventory(name='Item1', created_at=date1)
        create_inventory(name='Item2', created_at=date2)
        create_inventory(name='Item3', created_at=date3)

        url = reverse('inventory-list')

        # Test with a date that should exclude the first item
        response = api_client.get(url, {'created_after_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')})
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2  

        expected_data = InventorySerializer(Inventory.objects.filter(created_at__gt=datetime.now() - timedelta(days=7)), many=True).data
        assert data == expected_data

        # Test with a date that should include all items
        response = api_client.get(url, {'date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')})
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3  

        expected_data = InventorySerializer(Inventory.objects.all(), many=True).data
        assert data == expected_data

        # Test with an invalid date format
        response = api_client.get(url, {'date': 'invalid-date'})
        assert response.status_code == 400
        assert 'error' in response.json()

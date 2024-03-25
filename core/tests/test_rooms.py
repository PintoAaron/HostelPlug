import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Hostel, Room


@pytest.mark.django_db
class TestCreateRoom():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        hostel = baker.make(Hostel)
        data = {
                'capacity': "2 IN 1",
                'price': 1000,
                'available_beds': 1,
                }
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/rooms/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    def test_if_user_is_authenticated_but_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        hostel = baker.make(Hostel)
        data = {
                'capacity': "2 IN 1",
                'price': 1000,
                'available_beds': 1,
                }
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/rooms/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_staff_return_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        data = {
                'capacity':"2 IN 1",
                'price': 1000,
                'available_beds': 1,
                }
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/rooms/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
                'id': 1,
                'capacity': "2 IN 1",
                'price': 1000,
                'available_beds': 1,
                }
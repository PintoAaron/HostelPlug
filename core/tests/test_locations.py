import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Location


@pytest.mark.django_db
class TestCreateLocation():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        response = api_client.post('/api/v1/locations/', {'name': 'Test Location'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        response = api_client.post('/api/v1/locations/', {'name': 'Test Location'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_staff_return_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.post('/api/v1/locations/', {'name': 'Test Location'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Location'
        
    
    def test_if_user_is_staff_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.post('/api/v1/locations/', {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        


@pytest.mark.django_db
class TestListLocations():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        response = api_client.get('/api/v1/locations/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_staff_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        response = api_client.get('/api/v1/locations/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        response = api_client.get('/api/v1/locations/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['id'] == location.id
            


@pytest.mark.django_db
class TestRetriveLocation():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        location = baker.make(Location)
        response = api_client.get(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        location = baker.make(Location)
        response = api_client.get(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        response = api_client.get(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == location.id
        
    
    
    def test_if_user_is_staff_and_location_does_not_exist_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.get('/api/v1/locations/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
        


@pytest.mark.django_db
class TestUpdateLocation():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        location = baker.make(Location)
        response = api_client.patch(f'/api/v1/locations/{location.id}/', {'name': 'Updated Location'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        location = baker.make(Location)
        response = api_client.patch(f'/api/v1/locations/{location.id}/', {'name': 'Updated Location'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        response = api_client.patch(f'/api/v1/locations/{location.id}/', {'name': 'Updated Location'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Location'
        
    
    def test_if_user_is_staff_and_location_does_not_exist_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.patch('/api/v1/locations/100/', {'name': 'Updated Location'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
        
    
    
    def test_if_user_is_staff_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        response = api_client.patch(f'/api/v1/locations/{location.id}/', {'name': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        
        
        
        
@pytest.mark.django_db
class TestDeleteLocation():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        location = baker.make(Location)
        response = api_client.delete(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        location = baker.make(Location)
        response = api_client.delete(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    def test_if_user_is_staff_return_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        response = api_client.delete(f'/api/v1/locations/{location.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
    
    def test_if_user_is_staff_and_location_does_not_exist_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.delete('/api/v1/locations/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
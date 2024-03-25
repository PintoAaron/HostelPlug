import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Hostel, Location


@pytest.mark.django_db
class TestCreateHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        location = baker.make(Location)
        data = {'name': 'Test Hostel',
                'location': location.id,
                }
        response = api_client.post('/api/v1/hostels/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    def test_if_user_is_authenticated_but_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        location = baker.make(Location)
        data = {'name': 'Test Hostel',
                'location': location.id,
                }
        response = api_client.post('/api/v1/hostels/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    
    def test_if_user_is_staff_return_201(self, api_client, authenticate):
        authenticate(is_staff=True)
        location = baker.make(Location)
        data = {'name': 'Test Hostel',
                'location': location.id,
                }
        response = api_client.post('/api/v1/hostels/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Hostel'
        assert response.data['location'] == location.id
        
    
    def test_if_user_is_staff_and_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        data = {'name': 'Test Hostel',
                'location': 1,}
        response = api_client.post('/api/v1/hostels/',data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'location' in response.data
        


@pytest.mark.django_db
class TestListHostel():
    def test_if_user_is_not_authenticated_return_200(self, api_client):
        hostel = baker.make(Hostel)
        response = api_client.get('/api/v1/hostels/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('results')[0]['id'] == hostel.id
    
    
    def test_if_user_is_authenticated_but_not_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=False)
        hostel = baker.make(Hostel)
        response = api_client.get('/api/v1/hostels/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('results')[0]['id'] == hostel.id
    
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        response = api_client.get('/api/v1/hostels/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('results')[0]['id'] == hostel.id
        
    


@pytest.mark.django_db
class TestRetriveHostel():
    def test_if_user_is_not_authenticated_return_200(self, api_client):
        hostel = baker.make(Hostel)
        response = api_client.get(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == hostel.id
        
    
    def test_if_user_is_authenticated_but_not_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=False)
        hostel = baker.make(Hostel)
        response = api_client.get(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == hostel.id
        
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        response = api_client.get(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == hostel.id
        
    
    
    def test_if_hostel_does_not_exist_return_404(self, api_client):
        response = api_client.get('/api/v1/hostels/100/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    
    
@pytest.mark.django_db
class TestUpdateHostel:
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        hostel = baker.make(Hostel)
        data = {'name': 'Updated Hostel'}
        response = api_client.patch(f'/api/v1/hostels/{hostel.id}/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    
    def test_if_user_is_authenticated_but_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        hostel = baker.make(Hostel)
        data = {'name': 'Updated Hostel'}
        response = api_client.patch(f'/api/v1/hostels/{hostel.id}/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    
    
    def test_if_user_is_staff_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        data = {'name': 'Updated Hostel'}
        response = api_client.patch(f'/api/v1/hostels/{hostel.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Hostel'
        
    
    
    def test_if_hostel_does_not_exist_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.patch('/api/v1/hostels/1/', {'name': 'Updated Hostel'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
        
    
    def test_if_request_meethod_is_put_return_405(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        data = {'name': 'Updated Hostel'}
        response = api_client.put(f'/api/v1/hostels/{hostel.id}/', data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        


@pytest.mark.django_db
class TestDeleteHostel():
    def test_if_user_is_not_authenticated_return_401(self, api_client):
        hostel = baker.make(Hostel)
        response = api_client.delete(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 
        
    
    def test_if_user_is_authenticated_but_not_staff_return_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        hostel = baker.make(Hostel)
        response = api_client.delete(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    
    def test_if_user_is_staff_return_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        hostel = baker.make(Hostel)
        response = api_client.delete(f'/api/v1/hostels/{hostel.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        
    
    def test_if_hostel_does_not_exist_return_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.delete('/api/v1/hostels/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'
    
    
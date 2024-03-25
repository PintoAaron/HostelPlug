import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Hostel, Review



@pytest.mark.django_db
class TestCreateReview():
    def test_if_user_is_not_authenticated_return_401(self,api_client):
        hostel = baker.make(Hostel)
        data = {'rating':1,'review':'Test Review'}
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/reviews/',data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_if_user_is_authenticated_return_200(self,api_client,authenticate):
        authenticate()
        hostel = baker.make(Hostel)
        data = {'rating':2,'review':'Test Review'}
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/reviews/',data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == hostel.id
        
        
    def test_if_user_is_authenticated_but_invalid_data_return_400(self,api_client,authenticate):
        authenticate()
        hostel = baker.make(Hostel)
        data = {'rating':0,'review':'Test Review'}
        response = api_client.post(f'/api/v1/hostels/{hostel.id}/reviews/',data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data        
        
        
        

from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from .models import User, Hostel, Location, Room, Review
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .serializers import UserSerializer, HostelSerializer, LocationSerializer, RoomSerializer, HostelCreateSerialzer,ReviewSerializer




class UserViewSet(ModelViewSet):
    http_method_names = ['get','patch','delete','head','options']
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]        
    
    

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.annotate(hostel_count=Count('hostels')).all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser]
    

class HostelViewSet(ModelViewSet):
    queryset = Hostel.objects.select_related('location').annotate(room_count=Count('rooms')).order_by('name').all()
    serializer_class = HostelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['name','location__name']
    ordering_fields = ['name','room_count']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HostelSerializer
        return HostelCreateSerialzer
    
    

class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Room.objects.filter(hostel_id = self.kwargs['hostel_pk'])
    
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk']}


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(hostel_id=self.kwargs['hostel_pk']).select_related('user').order_by('-timestamp')
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk'],
                'user_id':self.request.user.id
                }
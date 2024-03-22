from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from .models import Hostel, Location, Room, Review, HostelImage
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .serializers import HostelSerializer, LocationSerializer, RoomSerializer, HostelCreateSerialzer,ReviewSerializer, HostelImageSerializer




class LocationViewSet(ModelViewSet):
    queryset = Location.objects.annotate(hostel_count=Count('hostels')).all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser]
    

class HostelViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','options']
    
    queryset = Hostel.objects.select_related('location').prefetch_related('rooms','images').annotate(room_count=Count('rooms')).order_by('name').all()
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
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return Room.objects.filter(hostel_id = self.kwargs['hostel_pk'])
    
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk']}


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(hostel_id=self.kwargs['hostel_pk']).select_related('user').order_by('-timestamp')
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk'],
                'user_id':self.request.user.id
                }
        
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'detail':'You do not have permission to update this post'},status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            print('You do not have permission to perform this action')
            return Response({'detail':'You do not have permission to delete this post'},status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs) 
        

class HostelImageViewSet(ModelViewSet):
    serializer_class = HostelImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return HostelImage.objects.filter(hostel_id=self.kwargs['hostel_pk']).order_by('-date_created')
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk']}
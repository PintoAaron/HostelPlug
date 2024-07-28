from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import Hostel, Location, Room, Review, HostelImage,CartItem, Cart, Booking
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .serializers import HostelSerializer, LocationSerializer, RoomSerializer, HostelCreateSerialzer,ReviewSerializer, HostelImageSerializer,CartItemSerializer,CreateCartItemSerializer,CartSerializer,UpdateCartItemSerializer,BookingItemSerializer,BookingSerializer,CreateBookingSerializer
from core.utils import upload




class LocationViewSet(ModelViewSet):
    queryset = Location.objects.annotate(hostel_count=Count('hostels')).all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser]
    
    @method_decorator(cache_page(15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @method_decorator(cache_page(60*5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

class HostelViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','options']
    
    queryset = Hostel.objects.select_related('location').prefetch_related('rooms','images').annotate(room_count=Count('rooms')).order_by('name').all()
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['name','location__name']
    ordering_fields = ['name','room_count']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['POST','PATCH']:
            return HostelCreateSerialzer
        return HostelSerializer
    
    @method_decorator(cache_page(15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @method_decorator(cache_page(15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
    

class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return Room.objects.filter(hostel_id = self.kwargs['hostel_pk'])
    
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk']}
    
    
    @method_decorator(cache_page(15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @method_decorator(cache_page(15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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
            return Response({'detail':'You do not have permission to delete this post'},status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs) 
        

class HostelImageViewSet(ModelViewSet):
    serializer_class = HostelImageSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAdminOrReadOnly]
    
    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60*2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        return HostelImage.objects.filter(hostel_id=self.kwargs['hostel_pk']).order_by('-date_created')
    
    def get_serializer_context(self):
        return {'hostel_id':self.kwargs['hostel_pk']}
    
    
    def create(self, request, *args, **kwargs):
        file = request.data.get('image')
        image_url = upload.upload_image_to_storage_bucket_and_produce_url(file)
        if not image_url:
            raise ValueError('Image upload failed')
        request.data['image_url'] = image_url
        
        return super().create(request, *args, **kwargs)
    


class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__room').all()




class CartItemViewSet(ModelViewSet):

    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.select_related('room').filter(cart_id=self.kwargs['cart_pk'])
    
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    
    

class BookingViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','options']
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBookingSerializer
        return BookingSerializer
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.prefetch_related('bookingitems__room').all()
        return Booking.objects.prefetch_related('bookingitems__room').filter(user_id=self.request.user.id)
    
    
    def create(self, request, *args, **kwargs):
        serializer = CreateBookingSerializer(data=request.data, context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        bookings = serializer.save()
        serializer = BookingSerializer(bookings)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
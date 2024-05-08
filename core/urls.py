from django.views.generic import TemplateView
from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('hostels',views.HostelViewSet,basename='hostels')
router.register('locations',views.LocationViewSet)
router.register('carts',views.CartViewSet,basename='carts')
router.register('bookings',views.BookingViewSet,basename='bookings')


hostel_router = routers.NestedDefaultRouter(router,'hostels',lookup='hostel')
hostel_router.register('rooms',views.RoomViewSet,basename='hostel-rooms')
hostel_router.register('reviews',views.ReviewViewSet,basename='hostel-reviews')
hostel_router.register('images',views.HostelImageViewSet,basename='hostel-images')


cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart-items')



urlpatterns = [
    
    path('api/v1/', include(router.urls)),
    path('api/v1/',include(hostel_router.urls)),
    path('api/v1/',include(cart_router.urls)),
    path('', TemplateView.as_view(template_name='core/index.html')),
    
]

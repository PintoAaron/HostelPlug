from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('hostels',views.HostelViewSet,basename='hostels')
router.register('locations',views.LocationViewSet)


hostel_router = routers.NestedDefaultRouter(router,'hostels',lookup='hostel')
hostel_router.register('rooms',views.RoomViewSet,basename='hostel-rooms')
hostel_router.register('reviews',views.ReviewViewSet,basename='hostel-reviews')



urlpatterns = [
    
    path('', include(router.urls)),
    path('',include(hostel_router.urls)),
    
]

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from . import models



@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','name','hostels_count']
    list_editable = ['name']
    search_fields = ['name']
    list_per_page = 10
    ordering = ['name']
    
    
    
    @admin.display(ordering='hostels_count')
    def hostels_count(self,location):
        return location.hostels_count
    
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(hostels_count=Count('hostels'))


@admin.register(models.Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['id','name','location','contact','rooms_count']
    search_fields = ['name','location__name']
    list_per_page = 10
    ordering = ['name']
    list_select_related = ['location']
    
    @admin.display(ordering='rooms_count')
    def rooms_count(self,hostel):
        return hostel.rooms_count
    
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(rooms_count=Count('rooms'))
    
    
    
@admin.register(models.HostelImage)
class HostelImageAdmin(admin.ModelAdmin):
    list_display = ['id','hostel','image_url','date_created']
    search_fields = ['hostel__name']
    list_per_page = 10
    ordering = ['date_created']
    list_select_related = ['hostel']
    


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','hostel','capacity','price','available_beds']
    list_editable = ['price','available_beds']
    search_fields = ['hostel__name','capacity']
    list_per_page = 10
    ordering = ['hostel']
    list_select_related = ['hostel']
    
    
    

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['timestamp','hostel','rating','review','user']
    search_fields = ['hostel__name']
    list_per_page = 10
    ordering = ['-timestamp']
    list_select_related = ['hostel','user']
    


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','phone','email','review_count']
    list_per_page = 10
    ordering = ['username']
    
    @admin.display(ordering='reviews_count')
    def review_count(self,user):
        return user.reviews_count
    
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(reviews_count=Count('reviews'))
    
    


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','user','payment_status','timestamp']
    search_fields = ['user__username']
    list_per_page = 10
    ordering = ['-timestamp']
    list_select_related = ['user']
    list_filter = ['payment_status']
    
    
    
@admin.register(models.BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ['id','booking_id','room','quantity_booked','unit_price','total_price']
    list_per_page = 10
    ordering = ['booking']
    list_select_related = ['booking','room']
    
    @admin.display(ordering='unit_price')
    def unit_price(self,booking_item):
        return f"Ghc {booking_item.room.price}"
    
    @admin.display(ordering='total_price')
    def total_price(self,booking_item):
        return f"Ghc {booking_item.room.price * booking_item.quantity}"
    
    @admin.display(ordering='quantity')
    def quantity_booked(self,booking_item):
        return booking_item.quantity
    
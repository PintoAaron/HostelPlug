from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import uuid




class Location(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class Hostel(models.Model):
    name = models.CharField(max_length=100,null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='hostels')
    description = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length=15,null=True)
    facilities = models.TextField(blank=True,null=True)
    longitude = models.FloatField(null=True,default=6.67474)
    latitude = models.FloatField(null=True,default=-1.57160)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class HostelImage(models.Model):
    hostel = models.ForeignKey(Hostel, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    
    ONE_IN_ONE = "1 IN 1"
    TWO_IN_ONE = "2 IN 1"
    THREE_IN_ONE = "3 IN 1"
    FOUR_IN_ONE = "4 IN 1"
    
    CAPACITY_CHOICES = [ (ONE_IN_ONE, '1 IN 1'), (TWO_IN_ONE, '2 IN 1'), (THREE_IN_ONE, '3 IN 1'), (FOUR_IN_ONE, '4 IN 1')]
    
    hostel = models.ForeignKey(Hostel, related_name='rooms', on_delete=models.CASCADE)
    capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES, default=FOUR_IN_ONE)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    available_beds = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.capacity}@{self.hostel.name}"



class User(AbstractUser):
    phone = models.CharField(max_length=15,null=False)
    email = models.EmailField(unique=True)
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    


class Review(models.Model):
    hostel = models.ForeignKey(Hostel, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(null=True,blank=True,default=3)
    review = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    
    def __str__(self):
        return f"{self.hostel.name} - {self.user.username} - {self.rating}"
    


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='cartitems', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1,validators=[MinValueValidator(1)])
    
    
    class Meta:
        unique_together = ['cart','room']
        
        


class Booking(models.Model):
    
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"
    
    STATUS = [(PAYMENT_PENDING, 'Pending'),
              (PAYMENT_COMPLETE, 'Complete'),
              (PAYMENT_FAILED, 'Failed')]
    
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.PROTECT)
    payment_status = models.CharField(max_length=1, choices= STATUS, default=PAYMENT_PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='bookingitems', on_delete=models.PROTECT)
    room = models.ForeignKey(Room, related_name='bookingitems', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1,validators=[MinValueValidator(1)])
  
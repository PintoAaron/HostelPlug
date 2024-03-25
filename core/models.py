from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_file_size



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
    available_beds = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.capacity}@{self.hostel.name}"



class User(AbstractUser):
    phone = models.CharField(max_length=15,null=False)
    
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
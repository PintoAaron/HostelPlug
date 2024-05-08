from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, Hostel, Location, Room, Review, HostelImage, CartItem, Cart




class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','username','password']
        
        
    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        self.instance = User.objects.create(**self.validated_data)
        self.instance.save()
        return self.instance
    

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','email','username','phone']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
    


class LocationSerializer(serializers.ModelSerializer):
    hostel_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Location
        fields = ['id','name','hostel_count']
        
        
class HostelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelImage
        fields = ['id','image_url']
        
    def create(self, validated_data):
        hostel_id = self.context['hostel_id']
        image_url = validated_data.pop('image_url')
        return HostelImage.objects.create(hostel_id=hostel_id, image_url=image_url)
    
    
    
class HostelSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    room_count = serializers.IntegerField(read_only=True)
    images = HostelImageSerializer(many=True,read_only=True)
    class Meta:
        model = Hostel
        fields = ['id','name','location','description','contact','facilities','room_count','images','longitude','latitude']
        



    
class HostelCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id','name','location','description','contact','facilities','longitude','latitude']
        
    
    
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','capacity','price','available_beds']
        
    
    def create(self, validated_data):
        hostel_id = self.context['hostel_id']
        return Room.objects.create(hostel_id=hostel_id,**validated_data)



class ReviewSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id','rating','review','timestamp','user']
       
    def validate(self, data):
        if data['rating'] < 1 or data['rating'] > 5:
            raise serializers.ValidationError("Rating should be between 1 to 5")
        return data
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        hostel_id = self.context['hostel_id']
        return Review.objects.create(hostel_id=hostel_id, user_id=user_id, **validated_data)
    


class CartItemSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','room','quantity','total_price']
        
    total_price = serializers.SerializerMethodField()
    
    
    def get_total_price(self, obj: CartItem):
        return obj.room.price * obj.quantity
    
    
    
    

class CreateCartItemSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','room_id','quantity']
        
    def validate_room_id(self, value):
        if not Room.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid Room ID")
        return value
        
    def validate(self, data):
        room = Room.objects.get(id=data['room_id'])
        if data['quantity'] > room.available_beds:
            raise serializers.ValidationError("Not enough beds available")
        return data
    
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        room_id = self.validated_data['room_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, room_id=room_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
    def validate(self, data):
        if data['quantity'] > data['room'].available_beds:
            raise serializers.ValidationError("Not enough beds available")
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
        
    id = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    
    def get_total_price(self, obj: Cart):
        return sum([item.room.price * item.quantity for item in obj.items.all()])
    
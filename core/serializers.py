from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, Hostel, Location, Room, Review, HostelImage




class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','password','phone']
        
        
    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        self.instance = User.objects.create(**self.validated_data)
        self.instance.save()
        return self.instance
    

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','phone']


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
        print(validated_data)
        image_url = validated_data.pop('image_url')
        print("we dey the serializer")
        print(image_url)
        return HostelImage.objects.create(hostel_id=hostel_id, image_url=image_url)
    
    
    
class HostelSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    room_count = serializers.IntegerField(read_only=True)
    images = HostelImageSerializer(many=True,read_only=True)
    class Meta:
        model = Hostel
        fields = ['id','name','location','description','contact','facilities','room_count','images']
        



    
class HostelCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id','name','location','description','contact','facilities',]
        
    
    
    
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
    



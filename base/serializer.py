from rest_framework import serializers
from .models import Event, Order, Purchase
from .models import UserInformation,EventImage
from django.contrib.auth.models import User 



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User 
        fields = ("id",'username','email', 'date_joined', 'is_superuser', 'date_joined')  


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for EventImage model.
    """
    class Meta:
        model=EventImage
        fields='__all__'   
 
class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """
    class Meta:
        model = Event
        fields = '__all__'

class UserInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for UserInformation model.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    print(user)
    class Meta:
        model = UserInformation
        fields= '__all__'
        def create(self, validated_data):
                user = self.context['user']
                print(user)
                return UserInformation.objects.create(**validated_data,user=user)

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    class Meta:
        model = Order
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for Purchase model.
    """
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'event', 'quantity', 'subtotal', 'date')
        read_only_fields = ('id', 'date_purchased')


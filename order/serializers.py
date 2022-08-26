from dataclasses import field
from rest_framework import serializers

from dishes.models import Dishes
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    dishes_title = serializers.ReadOnlyField(source='dishes.title')
    dishes = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ('dishes','quantity','dishes_title')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # repr.pop('dishes')
        return repr


class OrderSerializer(serializers.ModelSerializer):
    positions = OrderItemSerializer(write_only = True, many = True)
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source = 'user.email')
    class Meta:
        model = Order 
        fields = ('id','user','create_at', 'positions', 'status')

    def create(self, validated_data):
        dishes = validated_data.pop('positions')
        user = self.context.get('request').user 
        order = Order.objects.create(user = user, status='open')
        for dish in dishes:
            blyudo = dish['dishes']
            bluydo = Dishes.objects.get(pk=blyudo)
            quantity = dish['quantity']
            OrderItem.objects.create(order=order, dishes=bluydo, quantity=quantity)
        return order
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['dishes'] = OrderItemSerializer(instance.items.all(), many = True).data
        return repr

class HistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    class Meta:
        model = Order
        fields = ('id','user', 'dishes', 'create_at','status')
        
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['dishes'] = OrderItemSerializer(instance.items.all(), many = True).data
        return repr

    
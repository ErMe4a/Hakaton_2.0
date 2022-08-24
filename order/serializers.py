from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    dishes = serializers.ReadOnlyField(source='dishes.title')
    class Meta:
        model = OrderItem
        fields = ('dishes', 'quantity', 'dishes_title')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr.pop('dishes')
        return repr()


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
            dishes = dish['dishes']
            quantity = dish['quantity']
            OrderItem.objects.create(order=order, dishes=dishes, quantity=quantity)
        return order
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['dishes'] = OrderItemSerializer(instance.items.all(), many = True).data
        return repr
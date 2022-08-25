from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user =serializers.ReadOnlyField(source = 'user.email')
    dishes = serializers.ReadOnlyField(source = 'dishes.title')
    class Meta:
        model = Review
        fields = '__all__'

    def create(self , validated_data):
        request =self.context.get('request')
        user = request.user 
        dishes = self.context.get('dishes')
        validated_data['user'] = user
        validated_data['dishes'] = dishes
        return super().create(validated_data)
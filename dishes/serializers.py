from rest_framework import serializers
from .models import Dishes
from django.db.models import Avg


class DishesListSerializer(serializers.ModelSerializer):

    class Meta :
        model = Dishes
        fields = ('id','title', 'price', 'image')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr

class DishesDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Dishes
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr
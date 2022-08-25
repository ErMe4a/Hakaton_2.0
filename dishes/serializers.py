from rest_framework import serializers
from .models import Dishes
from django.db.models import Avg
from comments_and_likes.serializers import CommentSerializer


class DishesListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta :
        model = Dishes
        fields = ('id','title', 'price', 'image','comments')

    def is_liked(self,dishes):
        user = self.context.get('request').user
        return user.liked.filter(dishes=dishes).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr

class DishesDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta: 
        model = Dishes
        fields = '__all__'
    def is_liked(self,dishes):
        user = self.context.get('request').user
        return user.liked.filter(dishes=dishes).exists()
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr
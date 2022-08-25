from rest_framework import serializers
from .models import Comment,Like,Favorites
from dishes.models import Dishes


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = ('id','body','owner','dishes')


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Like
        fields =('owner',)
class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ('id','title','image',)
class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('dishes',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['dishes'] = DishesSerializer(instance.dishes).data
        return repr


from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from .models import Dishes
from . import serializers
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from comments_and_likes.serializers import CommentSerializer,LikeSerializer
from comments_and_likes.models import Like

import dishes
class DishesViewSet(ModelViewSet):
    queryset = Dishes.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DishesListSerializer
        return serializers.DishesDetailSerializer

    def get_permissions(self):
        # Создавать может залогиненный юзер
        if self.action in ( 'add_to_liked', 'remove_from_liked','get_likes', ):
            return [permissions.IsAuthenticated()]
        # Изменять и удалять может только автор поста
        elif self.action in ('update','create', 'partial_update', 'destroy', ):
            return [permissions.IsAdminUser()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny()]


    #api/v1/products/<id>/rewiews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        dishes = self.get_object()
        if request.method =='GET':
            reviews =  dishes.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status = 200)
        data = request.data 
        serializer = ReviewSerializer(data = data, context={'request':request, 'dishes':dishes})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=201)

        # api/v1/posts/<id>/comments/
    @action(['GET'], detail=True, )
    def comments(self, request, pk):
        dishes = self.get_object()
        comments = dishes.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=200)

    @action(['POST'], detail=True, )
    def add_to_liked(self, request, pk):
        dishes = self.get_object()
        if request.user.liked.filter(dishes=dishes).exists():
            return response.Response('Вы уже поставили свой лайк!', status=400)
        Like.objects.create(dishes=dishes, owner=request.user)
        return response.Response('Вы поставили лайк', status=201)

    # pai/v1/posts/<id>/remove_from_liked
    @action(['POST'], detail=True, )
    def remove_from_liked(self, request, pk):
        dishes = self.get_object()
        if not request.user.liked.filter(dishes=dishes).exists():
            return response.Response('Вы не лайкали этот пост', status=400)
        request.user.liked.filter(dishes=dishes).delete()
        return response.Response('Ваш лайк удален!', status=204)

    # api/v1/posts/<id>/get_likes
    @action(['GET'], detail=True, )
    def get_likes(self, request, pk):
        dishes = self.get_object()
        likes = dishes.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return response.Response(serializer.data, status=200)

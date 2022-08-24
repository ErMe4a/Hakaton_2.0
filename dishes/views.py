from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from .models import Dishes
from . import serializers
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from comments_and_likes.serializers import CommentSerializer

import dishes
class DishesViewSet(ModelViewSet):
    queryset = Dishes.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DishesListSerializer
        return serializers.DishesDetailSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (permissions.IsAdminUser,)
        return [permission() for permission in permission_classes]

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

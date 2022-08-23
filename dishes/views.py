from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from .models import Dishes
from . import serializers
from rest_framework.decorators import action
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

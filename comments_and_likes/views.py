from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from dishes.models import Dishes
from . import serializers
from .models import Comment



User = get_user_model()

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAdminUser,)
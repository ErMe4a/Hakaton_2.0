from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')


    class Meta:
        model = Comment
        fields = ('id','body','owner','dishes')
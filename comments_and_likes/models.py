from django.db import models
from account.models import CustomUser
from dishes.models import Dishes

class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='comments',on_delete=models.CASCADE)
    dishes = models.ForeignKey(Dishes,related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.dishes} -> {self.created_at}'

class Like(models.Model):
    dishes = models.ForeignKey(Dishes,on_delete=models.CASCADE,related_name='likes')
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='liked')
    class Meta:
        unique_together = ['dishes','owner']


class Favorites(models.Model):
    dishes = models.ForeignKey(Dishes,on_delete=models.CASCADE,related_name='favorites')
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='favorites')
    class Meta:
        unique_together = ['dishes','owner']


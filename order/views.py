from rest_framework import generics, permissions, response, views
from . import serializers 
from .models import Order
from account import permissions as per

class CreateOrderView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
class UserOrderList(views.APIView):
    permission_classes =(permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        orders = user.orders.all()
        serializer = serializers.OrderSerializer(orders, many =True).data
        return response.Response(serializer, status = 200)

class UpdateOrderStatusView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk):
        status = request.data['status']
        if status not in ['in_proces', 'closed']:
            return response.Response('Invalid Status', status = 400)
        order = Order.objects.get(pk=pk)
        order.status = status
        order.save()
        serializer = serializers.OrderSerializer(order).data
        return response.Response(serializer, status = 206)

class HistoryView(views.APIView):
    permission_classes =(per.IsAccountOwner, )

    def get(self, request):
        user = request.user
        orders = user.orders.all()
        serializer = serializers.HistorySerializer(orders, many =True).data 
        return response.Response(serializer, status = 200)

    
    def delete(self,request, pk):
        user = request.user
        user.orders.get(pk=pk).delete()
        return response.Response('Ваш заказ удалён!', status=204)



    

        



from django.urls import path
from order.serializers import HistorySerializer
from . import views

urlpatterns = [
    path('', views.CreateOrderView.as_view()),
    path('own/', views.UserOrderList.as_view()),
    path('<int:pk>/', views.UpdateOrderStatusView.as_view()),
    path('history/', views.HistoryView.as_view()),
    path('<int:pk>/history/', views.HistoryView.as_view()),
]
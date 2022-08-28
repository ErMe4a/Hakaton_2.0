from django.urls import path
from order.serializers import HistorySerializer
from . import views

urlpatterns = [
    path('', views.CreateOrderView.as_view()),
    path('<int:pk>/', views.UpdateOrderStatusView.as_view()),
    path('history/', views.OrderHistoryView.as_view()),
    path('<int:pk>/history/', views.OrderHistoryView.as_view()),
]
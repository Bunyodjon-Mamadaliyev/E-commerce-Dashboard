from django.urls import path
from .views import OrderViewSet


urlpatterns = [
    path('orders/<int:pk>/status/', OrderViewSet.as_view({'patch': 'status'}), name='order-status-update'),
]

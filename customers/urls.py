from django.urls import path
from .views import CustomerViewSet


urlpatterns = [
    path('customers/<int:pk>/orders/', CustomerViewSet.as_view({'get': 'orders'}), name='customer-orders'),
]

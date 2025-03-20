from django.urls import path, include
from rest_framework.routers import DefaultRouter
from categories.views import CategoryViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet
from customers.views import CustomerViewSet
from .views import DashboardStatsView, TopProductsView, TopCustomersView, RevenueStatsView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/top-products/', TopProductsView.as_view(), name='dashboard-top-products'),
    path('dashboard/top-customers/', TopCustomersView.as_view(), name='dashboard-top-customers'),
    path('dashboard/revenue/', RevenueStatsView.as_view(), name='dashboard-revenue'),

]




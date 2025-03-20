from django.urls import path
from .views import ProductImageViewSet


urlpatterns = [
    path('products/<int:product_id>/images/', ProductImageViewSet.as_view({'post': 'create'}), name='product-image-upload'),
    path('products/<int:product_id>/images/<int:image_id>/', ProductImageViewSet.as_view({'delete': 'destroy'}), name='product-image-delete'),
]

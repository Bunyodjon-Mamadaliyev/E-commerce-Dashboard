from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from customers.models import Customer
from products.serializers import ProductSerializer
from customers.serializers import CustomerSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'created_at']
        read_only_fields = ['created_at']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_price', 'shipping_address', 'payment_method', 'created_at', 'updated_at', 'items']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')

        if isinstance(customer_data, dict):
            customer, _ = Customer.objects.get_or_create(**customer_data)
        else:
            customer = Customer.objects.get(id=customer_data)  # Agar ID bo‘lsa, shunday ishlatamiz

        items_data = validated_data.pop('items', [])

        order = Order.objects.create(customer=customer, **validated_data)

        for item_data in items_data:
            product = Product.objects.get(id=item_data.pop('product'))
            OrderItem.objects.create(order=order, product=product, **item_data)

        return order


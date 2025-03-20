from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from common.pagination import DefaultPagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        order = Order.objects.create(
            customer_id=request.data["customer"],
            total_price=request.data["total_price"]
        )
        return Response({"message": "Order created successfully!"})

    def update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"detail": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({"detail": f"Order status updated to {new_status}"})
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

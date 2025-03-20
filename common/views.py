from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from django.db.models import Sum, Count
from orders.models import Order, OrderItem
from customers.models import Customer
from products.models import Product

class DashboardStatsView(APIView):
    def get(self, request):
        total_customers = Customer.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

        return Response({
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_revenue": total_revenue
        })


class TopProductsView(APIView):
    def get(self, request):
        top_products = OrderItem.objects.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]
        return Response(top_products)


class TopCustomersView(APIView):
    def get(self, request):
        top_customers = Order.objects.values('customer__user__username').annotate(total_spent=Sum('total_price')).order_by('-total_spent')[:5]
        return Response(top_customers)


class RevenueStatsView(APIView):
    def get(self, request):
        today = now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        daily_revenue = Order.objects.filter(created_at__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0
        weekly_revenue = Order.objects.filter(created_at__date__gte=week_ago).aggregate(Sum('total_price'))['total_price__sum'] or 0
        monthly_revenue = Order.objects.filter(created_at__date__gte=month_ago).aggregate(Sum('total_price'))['total_price__sum'] or 0

        return Response({
            "daily_revenue": daily_revenue,
            "weekly_revenue": weekly_revenue,
            "monthly_revenue": monthly_revenue
        })

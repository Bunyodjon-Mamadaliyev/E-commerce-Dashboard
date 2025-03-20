from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

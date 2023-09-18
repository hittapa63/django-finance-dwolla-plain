from django.contrib import admin

from .models import DwollaCustomer



@admin.register(DwollaCustomer)
class DwollaCustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'created_at']
    list_filter = ['created_at']

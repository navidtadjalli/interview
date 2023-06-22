from django.contrib import admin
from customer.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone_number', 'email', 'registered_at', 'last_login_at', )
    search_fields = ('last_name', 'first_name', 'phone_number',)
    readonly_fields = ('registered_at', 'last_login_at', )


admin.site.register(Customer, CustomerAdmin)

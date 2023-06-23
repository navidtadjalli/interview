from django.contrib import admin
from customer.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'last_name', 'first_name', 'email', 'date_joined', 'last_login', )
    search_fields = ('last_name', 'first_name', 'phone_number',)
    readonly_fields = ('date_joined', 'last_login', )


admin.site.register(Customer, CustomerAdmin)

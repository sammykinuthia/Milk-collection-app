from django.contrib import admin
from .models import Customer, Milk, MilkPricing, MpesaAuth, MpesaPayment


# payment function


# actions


@admin.action(description="pay selected customers")
def makepayment(Modeladmin, request, queryset):
    cus = []
    amount = []
    for x in queryset:
        if x.customer not in cus:
            cus.append(x.customer)
            amount.append(x.price)
        else:
            i = cus.index(x.customer)
            amount[i] += x.price

    # print(amount)


@admin.action(description="Mark as Inactive")
def mark_inactive(Modealadmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Mark as active")
def mark_active(Modealadmin, request, queryset):
    queryset.update(is_active=True)

# admin models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone',
                    'address', 'is_active', 'registered_on')
    exclude = ('registered_on', 'is_active')
    list_filter = ('is_active', 'address')
    actions = [mark_inactive, mark_active]


class MilkAdmin(admin.ModelAdmin):
    list_display = ('customer', 'quantity', 'is_payed',
                    'price', 'price_per_litre', 'date')
    list_filter = ('customer', 'date', 'is_payed')
    actions = [makepayment]


class MilkPricingAdmin(admin.ModelAdmin):
    list_display = ('date', 'buying_price')
    fields = ['buying_price']


@admin.register(MpesaAuth)
class MpesaAuthAdmin(admin.ModelAdmin):
    list_display = ['initiation_time', 'expiration_time', 'token']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Milk, MilkAdmin)
admin.site.register(MilkPricing, MilkPricingAdmin)
admin.site.register(MpesaPayment)

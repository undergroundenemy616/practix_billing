from django.contrib import admin
from subscribtions.models import Account, Payment, Tariff


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'expiration_dt', 'get_tariff',)

    list_filter = ('status', 'expiration_dt', 'tariff',)

    def get_tariff(self, obj):
        if obj.tariff:
            return obj.tariff.name


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'period', 'amount',)
    search_fields = ('description', 'amount')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bill', 'is_success',)
    list_filter = ('is_success', 'bill',)

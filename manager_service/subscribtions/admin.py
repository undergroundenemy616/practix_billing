from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subscribtions.models import Account, Payment, Tariff


@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'status', 'expiration_dt', 'get_tariff',)

    list_filter = ('status', 'expiration_dt', 'tariff',)

    def get_tariff(self, obj):
        if obj.tariff:
            return obj.tariff.name


@admin.register(Tariff)
class TariffAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'description', 'period', 'amount',)
    search_fields = ('description', 'amount')


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'bill', 'is_success',)
    list_filter = ('is_success', 'bill',)

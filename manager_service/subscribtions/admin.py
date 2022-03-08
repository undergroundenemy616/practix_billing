from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subscribtions.models import Account, Payment, Tariff, Bill


@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'status', 'expiration_dt', 'get_tariff',)

    list_filter = ('status', 'expiration_dt', 'tariff',)

    def get_tariff(self, obj):
        if obj.tariff:
            return obj.tariff.name
        return None


@admin.register(Tariff)
class TariffAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'description', 'period', 'amount',)
    search_fields = ('description', 'amount')


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'bill', 'is_success', 'info', 'transaction_id')
    list_filter = ('is_success', 'bill')


@admin.register(Bill)
class BillAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'status', 'ip_address', 'card_cryptogram_packet',
                    'pa_res', 'amount', 'paid_period', 'payment_type', 'account')
    list_filter = ('status', 'payment_type', 'account')
    search_fields = ('ip_address', 'card_cryptogram_packet', 'pa_res', )


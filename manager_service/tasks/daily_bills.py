from datetime import datetime, timedelta

from auth_grpc.set_role import set_auth_role
from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.db.models import F, Q
from subscribtions.models import Account, Bill, Payment


class DailyBillPayer:
    def __init__(self, account: Account):
        self.account = account
        self.subscribtion = self.account.tariff.name
        self.bill = None
        self.successful_payment = None

    def get_the_bill(self):
        bill, created = Bill.objects.get_or_create(
            account=self.account,
            status=Bill.BillStatuses.NOT_PAID
        )
        if created:
            bill.amount = self.account.tariff.amount
            bill.paid_period = self.tariff.period
        bill.status = Bill.BillStatuses.IN_WORK
        bill.save()
        return bill

    def pay_the_bill(self):
        try:
            payment_id = pay(self.bill.id)
        except Exception:
            return False

        try:
            return Payment.objects.get(id=payment_id).is_success
        except Payment.DoesNotExist:
            return False

    def update_db(self):

        with transaction.atomic():
            if self.successful_payment:
                self.account.status = Account.SubscriptionStatuses.ACTIVE
                self.account.expiration_dt = F('expiration_dt') + self.account.tariff.period
                self.bill.status = Bill.BillStatuses.PAID
            else:
                if self.bill.updated_at > self.bill.created_at + timedelta(days=settings.NOT_PAID_DAYS_EXPIRATION):
                    self.account.status = Account.SubscriptionStatuses.CANCELED
                    self.subscribtion = "BaseUser"
                else:
                    self.account.status = Account.SubscriptionStatuses.OVERDUE
                self.bill.status = Bill.BillStatuses.NOT_PAID
            self.account.save()
            self.bill.save()

    def change_role(self):
        set_auth_role(id_=self.account.id, role=self.subscribtion)

    def run(self):
        self.bill = self.get_the_bill()
        self.successful_payment = self.pay_the_bill()
        self.update_db()
        self.change_role()


@shared_task
def create_daily_bills():
    accounts = Account.objects.filter(Q(expiration_dt=datetime.now().date()) |
                                      Q(status=Account.SubscriptionStatuses.OVERDUE)).exclude(tariff__isnull=True)

    for account in accounts:
        DailyBillPayer(account).run()

import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Дата + время создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата + время обновления'), auto_now=True)

    class Meta:
        abstract = True


class Tariff(BaseModel):

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    class TariffNames(models.TextChoices):
        SUBSCRIBER = 'Subscriber'

    class PeriodTypes(models.Choices):
        WEEK = timedelta(days=7)
        MONTH = timedelta(days=30)
        YEAR = timedelta(days=356)

    name = models.CharField(
        _('Название подписки'),
        max_length=256,
        null=False,
        blank=True,
        choices=TariffNames.choices
    )
    description = models.TextField(_('Описание'), null=True, blank=True)
    period = models.DurationField(_('Период'), choices=PeriodTypes.choices, default=PeriodTypes.MONTH)
    amount = models.PositiveIntegerField(_('Цена'), null=False, blank=True)


class Account(BaseModel):

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    class SubscriptionStatuses(models.TextChoices):
        ACTIVE = 'Active'
        OVERDUE = 'Overdue'
        CANCELED = 'Canceled'

    status = models.TextField(_('Статус'), choices=SubscriptionStatuses.choices, db_index=True)
    payment_token = models.TextField(_('Платежный токен'), null=True, blank=True, unique=True)
    expiration_dt = models.DateField(_('Дата окончания'), null=True, blank=True)
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accounts'
    )

    def cancel_subscribe(self):
        self.status = self.SubscriptionStatuses.CANCELED
        self.expiration_dt = None
        self.tariff = None
        self.save()


class Bill(BaseModel):

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    class BillStatuses(models.TextChoices):
        PAID = 'Paid'
        IN_WORK = 'In work'
        NOT_PAID = 'Not paid'

    class PaymentType(models.TextChoices):
        CRYPTOGRAM = 'Cryptogram'
        TOKEN = 'Token'
        POST3DS = '3DS'

    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        db_index=True,
        editable=False
    )
    status = models.TextField(_('Статус'), choices=BillStatuses.choices, default=BillStatuses.IN_WORK)
    payment_type = models.TextField(_('Тип платежа'), choices=PaymentType.choices, null=False, blank=True)
    ip_address = models.TextField(_('IP адрес'), null=True, blank=True)
    card_cryptogram_packet = models.TextField(_('Криптограмма'), null=True, blank=True)
    pa_res = models.TextField(_('Pa Res'), null=True, blank=True)
    amount = models.PositiveIntegerField(_('Сумма к оплате'), null=False, blank=True, editable=False)
    paid_period = models.DurationField(_('Оплачиваемый период'), null=False, blank=True, editable=False, default=timedelta(days=30))


class Payment(BaseModel):

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    bill = models.ForeignKey(
        Bill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        editable=False
    )
    transaction_id = models.PositiveIntegerField(_('ID транзакции'), null=True, blank=True)
    is_success = models.BooleanField(_('Статус'), null=False, default=False, blank=True)
    info = models.TextField(_('Информация'), null=True, blank=True)

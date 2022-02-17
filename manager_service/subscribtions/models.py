from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Дата + время создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата + время обновления'), auto_now=True)

    class Meta:
        abstract = True


class Tariff(BaseModel):
    class TariffNames(models.TextChoices):
        SUBSCRIBER = 'Subscriber'

    class PeriodTypes(models.TextChoices):
        WEEK = 'Week'
        MONTH = 'Month'
        YEAR = 'Year'

    name = models.CharField(
        _('Название подписки'),
        max_length=256,
        null=False,
        blank=True,
        choices=TariffNames.choices
    )
    description = models.TextField(null=True, blank=True)
    period = models.TextField(_('Период подписки'), choices=PeriodTypes.choices, default=PeriodTypes.MONTH)
    amount = models.PositiveIntegerField(_('Цена подписки'), null=False, blank=True)


class Account(BaseModel):
    class SubscriptionStatuses(models.TextChoices):
        ACTIVE = 'Active'
        OVERDUE = 'Overdue'
        CANCELED = 'Canceled'

    status = models.TextField(_('Статус подписки'), choices=SubscriptionStatuses.choices, db_index=True)
    payment_token = models.TextField(_('Платежный токен'), null=True, blank=True, unique=True)
    expiration_dt = models.DateField(_('Дата окончания подписки'), null=True, blank=True)
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accounts'
    )


class Bill(BaseModel):
    class BillStatuses(models.TextChoices):
        PAID = 'Paid'
        IN_WORK = 'In work'
        NOT_PAID = 'Not paid'

    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        db_index=True
    )
    status = models.TextField(_('Статус подписки'), choices=BillStatuses.choices)
    amount = models.PositiveIntegerField(_('Сумма к оплате'), null=False, blank=True)
    paid_period = models.DurationField(_('Оплачиваемый период'), null=False, blank=True)
    due_dt = models.DateField(_('Срок оплаты'), null=False, blank=True)

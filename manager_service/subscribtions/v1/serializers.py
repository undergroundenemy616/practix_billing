from django.db.models import F
from rest_framework import serializers, status
from rest_framework.response import Response
from subscribtions.models import Account, Bill, Payment, Tariff
from django.db import transaction
from tasks.worker import make_payment_on_bill


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ['id', 'amount', 'paid_period']


class PaymentSerializer(serializers.ModelSerializer):
    bill = BillSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class TariffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tariff
        fields = '__all__'


class BaseSubscriptionSerializer(serializers.ModelSerializer):
    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects.all(), required=True, allow_null=False)

    class Meta:
        model = Account
        exclude = ['created_at', 'updated_at', 'payment_token']
        read_only_fields = ['id', 'status', 'expiration_dt',
                            'created_at', 'updated_at']


class CreateSubscriptionSerializer(BaseSubscriptionSerializer):
    cryptogram = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if self.context['request'].user.status == Account.SubscriptionStatuses.ACTIVE:
            raise serializers.ValidationError('User already has active subscription')

    @transaction.atomic()
    def update(self, instance, validated_data):
        bill = Bill.objects.create(account=instance,
                                   payment_type=Bill.PaymentType.CRYPTOGRAM,
                                   ip_address=self.context['request'].headers['X-Real-IP'],
                                   card_cryptogram_packet=validated_data['cryptogram'],
                                   paid_period=validated_data['tariff'].period,
                                   amount=validated_data['tariff'].amount)
        make_payment_on_bill.delay(bill_uuid=bill.id)
        updated_bill = Bill.objects.filter(id=bill.id).first()
        if updated_bill.BillStatuses.IN_WORK:
            payment = Payment.objects.filter(bill=updated_bill, is_success=False).first()
            return Response(data={'message': payment.info,
                                  'result': 'error'},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.status = instance.SubscriptionStatuses.ACTIVE
        instance.tariff = validated_data['tariff']
        instance.expiration_dt = F('expiration_dt') + instance.tariff.period
        instance.save()
        return instance

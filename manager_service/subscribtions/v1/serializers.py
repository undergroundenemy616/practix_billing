from rest_framework import serializers, status
from rest_framework.response import Response
from subscribtions.models import Account, Bill, Payment, Tariff
from tasks.create_sub import create_sub


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


class SubscriptionSerializer(serializers.ModelSerializer):
    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects.all(), required=True, allow_null=False)

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'status', 'payment_token', 'expiration_dt']


class CreateSubscriptionSerializer(serializers.Serializer):
    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects.all(), required=True, allow_null=False)
    cryptogram = serializers.CharField(required=True)

    def validate(self, attrs):
        if self.context['request'].user.expiration_dt:
            raise serializers.ValidationError('User already has active subscription')

    def create(self, validated_data):
        account, result, message = create_sub(self.context['request'].user, **validated_data)
        if not result:
            return Response(data={'message': message,
                                  'result': result},
                            status=status.HTTP_400_BAD_REQUEST)
        return account

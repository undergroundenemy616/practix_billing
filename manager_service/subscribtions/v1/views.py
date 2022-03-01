from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from subscribtions.models import Account, Payment, Tariff
from subscribtions.v1.serializers import (CreateSubscriptionSerializer,
                                          PaymentSerializer,
                                          BaseSubscriptionSerializer,
                                          TariffSerializer)
from utils.pagination import DynamicPageNumberPagination
from utils.no_patch_api_views import UpdateAPIView, RetrieveUpdateDestroyAPIView


class SubscriptionView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.select_related('tariff')
    permission_classes = [IsAuthenticated]
    serializer_class = BaseSubscriptionSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CreateSubscriptionSerializer
        return self.serializer_class

    def perform_destroy(self, instance):
        instance.cancel_subscribe()

    def get_object(self):
        return self.request.user


class ChangeTariffSubscriptionView(UpdateAPIView):
    queryset = Account.objects.select_related('tariff')
    permission_classes = [IsAuthenticated]
    serializer_class = BaseSubscriptionSerializer


class TariffViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Tariff.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TariffSerializer


class PaymentViewSet(GenericViewSet,
                     ListModelMixin):
    queryset = Payment.objects.select_related('bill')
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    pagination_class = DynamicPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(bill__account=self.request.user)

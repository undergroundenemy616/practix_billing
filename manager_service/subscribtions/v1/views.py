from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from subscribtions.models import Account, Bill, Payment, Tariff
from subscribtions.v1.serializers import (CreateSubscriptionSerializer,
                                          PaymentSerializer,
                                          SubscriptionSerializer,
                                          TariffSerializer)
from utils.pagination import DynamicPageNumberPagination


class SubscriptionViewSet(GenericViewSet,
                          CreateModelMixin,
                          RetrieveModelMixin,
                          DestroyModelMixin,
                          UpdateModelMixin):
    queryset = Account.objects.select_related('tariff')
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateSubscriptionSerializer
        return self.serializer_class

    def perform_destroy(self, instance):
        instance.cancel_subscribe()


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

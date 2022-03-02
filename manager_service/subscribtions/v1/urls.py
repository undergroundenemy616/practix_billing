from django.urls import path
from subscribtions.v1 import views

urlpatterns = [
    path('tariffs', views.TariffViewSet.as_view({'get': 'list'}), name='tariffs_list'),
    path('payments', views.PaymentViewSet.as_view({'get': 'list'}), name='payment_list'),
    path('subscription', views.SubscriptionView.as_view(), name='subscriptions'),
    path('subscription/change-tariff', views.ChangeTariffSubscriptionView.as_view(), name='change-tariff')
]

from django.urls import path
from subscribtions.v1 import views
from utils.no_patch_router import NoPatchRouter

subscription_router = NoPatchRouter(trailing_slash=False)
subscription_router.register(r'v1/subscriptions', views.SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('tariffs', views.TariffViewSet.as_view({'get': 'list'}), name='tariffs_list'),
    path('payments', views.PaymentViewSet.as_view({'get': 'list'}), name='payment_list'),
]

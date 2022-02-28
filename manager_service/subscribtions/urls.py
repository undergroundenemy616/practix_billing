from django.urls import include, path
from subscribtions.v1.urls import subscription_router

urlpatterns = [
    path('v1/', include('subscribtions.v1.urls')),
]

urlpatterns += subscription_router.urls

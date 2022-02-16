from django.urls import path, include

urlpatterns = [
    path('v1/', include('subscribtions.v1.urls')),
]

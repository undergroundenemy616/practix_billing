from django.urls import include, path

urlpatterns = [
    path('v1/', include('subscribtions.v1.urls')),
]

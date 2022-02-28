from typing import Any

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.host = f'127.0.0.1:8001'
        return schema


def get_swagger() -> Any:
    swagger = get_schema_view(
        openapi.Info(
            title="Graduate Work API",
            default_version='v1',
            contact=openapi.Contact(email="undergroundenemy616@yandex.ru"),
        ),
        public=True,
        generator_class=APISchemeGenerator
    )
    return swagger


schema_view = get_swagger()

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include('subscribtions.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ]

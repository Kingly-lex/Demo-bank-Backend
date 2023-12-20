from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.common.views import GenerateNewAccountNo

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Demo Bank APP Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lexmail.aa@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # docs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # rest framework
    path('api-auth/', include('rest_framework.urls')),

    # auth
    path('api/v1/', include('apps.users.urls')),

    # admin
    path("admin/", admin.site.urls),

    # custom generate acct_no
    path('generate/', GenerateNewAccountNo.as_view(), name='generate_account_no'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Bank-APP"
admin.site.site_title = "Bank-APP Portal"
admin.site.index_title = "Welcome to BANK-APP Portal"

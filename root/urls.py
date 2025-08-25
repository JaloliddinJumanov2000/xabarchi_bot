from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import IsAdminUser
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EduBot API",
        default_version="v1",
        description="O'quvchilar va testlarni boshqarish API",
    ),
    public=True,
    permission_classes=(IsAdminUser,),   # 🔒 faqat admin
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),   # 🔹 API lar
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

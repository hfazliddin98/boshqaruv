from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Boshqaruv",
      default_version='v1.1',
      description="Boshqaruv uchun yaratilgan API",
      terms_of_service="https://kspi.uz",
      contact=openapi.Contact(email="hatamovfazliddin5@gmail.com"),
      license=openapi.License(name="KSPI License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
   path('haker/', admin.site.urls),
   path('api/token/', TokenObtainPairView.as_view(), name='token'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('', include('users.urls')),
   path('topshiriq/', include('topshiriq.urls')),

   # swagger
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
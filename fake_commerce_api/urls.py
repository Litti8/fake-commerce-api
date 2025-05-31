
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from products import views
from products.views import CategoryListView


from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = DefaultRouter()


router.register(r'products', views.ProductViewSet, basename='product')

# URL patterns 
urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('api/', include(router.urls)), 
    path('api/categories/', CategoryListView.as_view(), name='category-list'), 

    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI: Swagger UI (interactivo)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Optional UI: ReDoc (más enfocado a la lectura)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
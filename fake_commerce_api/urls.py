
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from products import views
from products.views import CategoryListView 


router = DefaultRouter()

# Registrar nuestro ProductViewSet con el router.
router.register(r'products', views.ProductViewSet, basename='product')

# URL patterns principales del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
]

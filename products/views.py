from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle 

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for product listings.
    Allows client to control page size via query parameter.
    """
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing read-only product data.
    Provides list and retrieve actions.
    """
    queryset = Product.objects.all().select_related('category').order_by('id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title']
    throttle_classes = [AnonRateThrottle] 


#View for listing Categories as a separate endpoint
class CategoryListView(generics.ListAPIView):
    """
    A view to list all product categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle] 
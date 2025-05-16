
from rest_framework import serializers
from products.models import Category, Product

# Serializador para el modelo Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

# Serializador para el modelo Product
class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
    
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'category', 'sizes']
        
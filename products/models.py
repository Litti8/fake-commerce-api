from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories" # Corrige el nombre en el admin

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sizes = models.CharField(max_length=255, help_text="Comma separated sizes, e.g., S,M,L,XL")
    

    def __str__(self):
        return self.title


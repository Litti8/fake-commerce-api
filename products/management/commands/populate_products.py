# products/management/commands/populate_products.py

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify 
from faker import Faker
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Populates the database with fake categories and products.'

    def add_arguments(self, parser):
        # Argumento opcional para especificar cuántos productos crear
        parser.add_argument(
            '--num_products',
            type=int,
            default=100, # Valor por defecto: 100 productos
            help='The number of fake products to create.',
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_products = options['num_products']

        self.stdout.write(self.style.SUCCESS('Deleting all existing products and categories...'))
        # Opcional: Eliminar datos existentes para empezar limpio cada vez
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        # Crear categorías 
        category_names = ['Clothing', 'Footwear', 'Accessories', 'Electronics', 'Books', 'Home & Kitchen'] # Ampliaremos para tener variedad si Faker lo permite
        category_objects = {}

        self.stdout.write(self.style.SUCCESS('Creating categories...'))
        for cat_name in category_names:
            # Asegurarnos que la categoría no exista ya 
            category, created = Category.objects.get_or_create(name=cat_name, defaults={'description': fake.sentence()})
            category_objects[cat_name] = category
            if created:
                self.stdout.write(f'Created category: {cat_name}')
            else:
                 self.stdout.write(f'Category already exists: {cat_name}') # No debería pasar si borramos antes

        # Usaremos solo las categorías de ropa, calzado, accesorios para los productos
        allowed_categories = [category_objects['Clothing'], category_objects['Footwear'], category_objects['Accessories']]
        if not allowed_categories:
             self.stdout.write(self.style.ERROR('No relevant categories found to assign products to.'))
             return

        self.stdout.write(self.style.SUCCESS(f'Creating {num_products} fake products...'))

        sizes_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'One Size', '36', '37', '38', '39', '40', '41', '42', '43', '44'] # Ejemplo de tallas
        product_images = [ # Ejemplos de URLs de imágenes
            'https://via.placeholder.com/400x300?text=Clothing',
            'https://via.placeholder.com/400x300?text=Shoes',
            'https://via.placeholder.com/400x300?text=Accessory',
            'https://via.placeholder.com/400x300?text=Product+1',
            'https://via.placeholder.com/400x300?text=Product+2',
            
        ]


        for i in range(num_products):
            # Seleccionar una categoría aleatoria de las permitidas
            category = random.choice(allowed_categories)

            # Generar datos de producto usando Faker
            if category.name == 'Clothing':
                product_title = fake.word().capitalize() + ' ' + fake.word().capitalize() + ' T-Shirt'
                product_description = fake.paragraph(nb_sentences=5)
                product_price = random.uniform(10.0, 80.0)
                product_image = random.choice([img for img in product_images if 'Clothing' in img or 'Product' in img])
                product_sizes = random.sample([s for s in sizes_options if s in ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'One Size']], k=random.randint(1, 4))
            elif category.name == 'Footwear':
                product_title = fake.word().capitalize() + ' ' + fake.word().capitalize() + ' Shoes'
                product_description = fake.paragraph(nb_sentences=5)
                product_price = random.uniform(30.0, 150.0)
                product_image = random.choice([img for img in product_images if 'Shoes' in img or 'Product' in img])
                product_sizes = random.sample([s for s in sizes_options if s.isdigit()], k=random.randint(3, 6))
            elif category.name == 'Accessories':
                product_title = fake.word().capitalize() + ' ' + fake.word().capitalize() + ' Accessory'
                product_description = fake.paragraph(nb_sentences=5)
                product_price = random.uniform(5.0, 60.0)
                product_image = random.choice([img for img in product_images if 'Accessory' in img or 'Product' in img])
                product_sizes = ['One Size'] if random.random() > 0.5 else random.sample([s for s in sizes_options if not s.isdigit()], k=random.randint(1, 3)) # Mezclar un poco
            else: # Para otras categorías si las incluimos (Electronics, Books, etc.)
                 product_title = fake.catch_phrase() + ' ' + fake.word()
                 product_description = fake.paragraph(nb_sentences=5)
                 product_price = random.uniform(1.0, 1000.0)
                 product_image = random.choice([img for img in product_images if 'Product' in img])
                 product_sizes = 'N/A'


            Product.objects.create(
                category=category,
                title=product_title,
                description=product_description,
                price=round(product_price, 2), # Redondear a 2 decimales
                image=product_image,
                sizes=','.join(product_sizes) if isinstance(product_sizes, list) else product_sizes
            )

            # Mostrar progreso ocasionalmente
            if (i + 1) % 50 == 0:
                 self.stdout.write(f'Created {i + 1}/{num_products} products...')


        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_products} products.'))
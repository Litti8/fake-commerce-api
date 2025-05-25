# products/management/commands/populate_products.py

import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Category, Product

class Command(BaseCommand):
    help = 'Populates the database with fake categories and products.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_products',
            type=int,
            default=100,
            help='The number of fake products to create.'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting all existing products and categories...'))
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        fake = Faker()
        num_products = options['num_products']

        self.stdout.write(self.style.MIGRATE_HEADING('Creating categories...'))
        categories_data = [
            {'name': 'Clothing', 'description': 'Fashionable apparel for all seasons.'},
            {'name': 'Footwear', 'description': 'Comfortable and stylish shoes for every occasion.'},
            {'name': 'Accessories', 'description': 'Enhance your look with our unique accessories.'},
            {'name': 'Electronics', 'description': 'Innovative gadgets and devices for modern living.'},
            {'name': 'Books', 'description': 'Explore worlds of knowledge and imagination.'},
            {'name': 'Home & Kitchen', 'description': 'Essentials and decor for your living space.'},
        ]
        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        self.stdout.write(self.style.MIGRATE_HEADING(f'Creating {num_products} fake products...'))

        # List of placeholder image URLs for variety
        # You can add more URLs here or change them
        PLACEHOLDER_IMAGE_URLS = [
            "https://placehold.co/400x300/E0F2F7/2C3E50?text=Product+1",
            "https://placehold.co/400x300/D1E8E4/2C3E50?text=Product+2",
            "https://placehold.co/400x300/C2DEDC/2C3E50?text=Product+3",
            "https://placehold.co/400x300/B3D4D4/2C3E50?text=Product+4",
            "https://placehold.co/400x300/A4CACB/2C3E50?text=Product+5",
            "https://placehold.co/400x300/95C0C2/2C3E50?text=Product+6",
            "https://placehold.co/400x300/86B6B9/2C3E50?text=Product+7",
            "https://placehold.co/400x300/77ACAF/2C3E50?text=Product+8",
            "https://placehold.co/400x300/68A2A6/2C3E50?text=Product+9",
            "https://placehold.co/400x300/59989D/2C3E50?text=Product+10",
        ]

        for i in range(num_products):
            category = random.choice(categories)
            title = fake.catch_phrase()
            description = fake.paragraph(nb_sentences=5)
            price = Decimal(random.uniform(5.00, 500.00)).quantize(Decimal('0.01'))
            sizes = ','.join(random.sample(['XS', 'S', 'M', 'L', 'XL', 'XXL', 'One Size', '36', '38', '40', '42', '43', '44'], k=random.randint(1, 4)))
            
            # Select a random image URL from our list
            image_url = random.choice(PLACEHOLDER_IMAGE_URLS)

            Product.objects.create(
                category=category,
                title=title,
                description=description,
                price=price,
                sizes=sizes,
                image=image_url
            )
            if (i + 1) % (num_products // 5) == 0:
                self.stdout.write(self.style.SUCCESS(f'Created {i + 1}/{num_products} products...'))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_products} products.'))

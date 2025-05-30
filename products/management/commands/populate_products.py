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

        # URLs de imágenes de Cloudinary organizadas por categoría
        CLOUDINARY_IMAGE_URLS = {
            "Clothing": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619439/unnamed_lbl57e.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619439/shirt-1_k4855p.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619439/jean-1_hba77o.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619438/hoodie_gltmbq.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619438/black-dress_c2g1jw.jpg"
            ],
            "Footwear": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619555/tennis_uf8cmj.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619555/tennis-2_teacej.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619554/flat-shoes_qero8w.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619554/descarga_xvrgex.jpg", # Nota: "descarga" puede no ser un nombre muy descriptivo
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619554/boots_liffs7.jpg"
            ],
            "Accessories": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619568/wallet_dqjn2q.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619568/watch_xfj7qi.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619567/sunglasses_ja3qcb.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619566/earrings-pendant-necklace_ltuhea.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619565/backpack_jbukyz.jpg"
            ],
            "Electronics": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619582/smartphone_t6mi1z.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619581/mouse_azndux.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619580/laptop_xkj5dd.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619580/headphones_xykmvh.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619579/camera_cgqr7q.jpg"
            ],
            "Books": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619593/minimalist-novel_rneiny.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619592/fantasy-novel_ghltxn.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619592/cookbook_lyswwx.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619591/books_g8sro6.jpg"
            ],
            "Home & Kitchen": [
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619603/plant_g1aigl.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619602/pillow_wgkdpi.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619601/lamp_gj1lwa.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619600/kitchen_gvzjs4.jpg",
                "https://res.cloudinary.com/duopj8det/image/upload/v1748619600/coffee-mug_li68kx.jpg"
            ]
        }
        # URL de placeholder por si alguna categoría no tiene imágenes definidas
        DEFAULT_PLACEHOLDER = "https://placehold.co/400x300/E0F2F7/2C3E50?text=Product+Image"


        for i in range(num_products):
            category = random.choice(categories)
            title = fake.catch_phrase()
            description = fake.paragraph(nb_sentences=5)
            price = Decimal(random.uniform(5.00, 500.00)).quantize(Decimal('0.01'))
            sizes = ','.join(random.sample(['XS', 'S', 'M', 'L', 'XL', 'XXL', 'One Size', '36', '38', '40', '42', '43', '44'], k=random.randint(1, 4)))
            
            # Selecciona una URL de imagen de Cloudinary de la categoría correspondiente
            image_url = random.choice(CLOUDINARY_IMAGE_URLS.get(category.name, [DEFAULT_PLACEHOLDER]))

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


from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status 
from decimal import Decimal 
from django.urls import reverse 

from products.models import Category, Product

class ProductAPITestCase(APITestCase):
    """
    Test suite for the Product and Category API endpoints.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        Creates categories and products with predictable attributes.
        """
        # Create some categories
        self.category1 = Category.objects.create(name='Category 1', description='Description 1')
        self.category2 = Category.objects.create(name='Category 2', description='Description 2')

        # Create some products
        self.product1 = Product.objects.create(
            category=self.category1,
            title='Product A',
            description='Description of Product A related to topic1',
            price=Decimal('10.00'),
            sizes='S,M,L',
            image='http://example.com/img1.jpg'
        )
        self.product2 = Product.objects.create(
            category=self.category1,
            title='Product B',
            description='Description of Product B related to topic2',
            price=Decimal('20.00'),
            sizes='XL',
             image='http://example.com/img2.jpg'
        )
        self.product3 = Product.objects.create(
            category=self.category2,
            title='Product C',
            description='Description of Product C related to topic1',
            price=Decimal('15.00'),
            sizes='One Size',
             image='http://example.com/img3.jpg'
        )
        self.product4 = Product.objects.create(
            category=self.category2,
            title='Unique Item Z',
            description='Another description for Z related to topic2',
            price=Decimal('25.00'),
            sizes='S',
             image='http://example.com/img4.jpg'
        )

        # Define base URLs for the API endpoints
        self.product_list_url = '/api/products/'
        self.category_list_url = '/api/categories/'


    # --- Model Tests ---

    def test_category_creation(self):
        """Test that a Category can be created."""
        category = Category.objects.create(name='New Category', description='New Description')
        self.assertEqual(Category.objects.count(), 3) # Already 2 categories from setUp
        self.assertEqual(category.name, 'New Category')

    def test_product_creation(self):
        """Test that a Product can be created."""
        product = Product.objects.create(
            category=self.category1,
            title='New Product',
            description='New Description',
            price=Decimal('99.99'),
            sizes='XS',
            image='http://example.com/new.jpg'
        )
        self.assertEqual(Product.objects.count(), 5) # Already 4 products from setUp
        self.assertEqual(product.title, 'New Product')
        self.assertEqual(product.category, self.category1)
        self.assertEqual(product.price, Decimal('99.99'))


    # --- API Tests (Product List) ---

    def test_product_list_status_code(self):
        """Test that the product list endpoint returns a 200 OK status code."""
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_pagination(self):
        """Test that the product list is paginated and returns expected keys."""
        response = self.client.get(self.product_list_url + '?page_size=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data # Accedemos a los datos deserializados de la respuesta

        self.assertIn('count', data)
        self.assertIn('next', data)
        self.assertIn('previous', data)
        self.assertIn('results', data)

        self.assertEqual(data['count'], 4) # Total number of products
        self.assertEqual(len(data['results']), 2) # Number of products on this page


    def test_product_list_filter_by_category_id(self):
        """Test filtering products by category ID."""
        # Add page_size to ensure pagination wrapper is included in test response
        response = self.client.get(f'{self.product_list_url}?category={self.category1.id}&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data['count'], 2) # product1 and product2 are in category1
        self.assertEqual(len(data['results']), 2)
        # Check that all returned products are from category1
        for product_data in data['results']:
            self.assertEqual(product_data['category']['id'], self.category1.id)


    def test_product_list_search(self):
        """Test searching products by title or description."""
        # Search by title - Add page_size to ensure pagination wrapper
        response = self.client.get(self.product_list_url + '?search=Unique Item Z&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'Unique Item Z')

        # Search by description - Add page_size to ensure pagination wrapper
        response = self.client.get(self.product_list_url + '?search=topic1&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 2) # product1 and product3 have 'topic1'
        titles = [p['title'] for p in data['results']]
        self.assertIn('Product A', titles)
        self.assertIn('Product C', titles)

    def test_product_list_ordering(self):
        """Test ordering products by price."""
        # Order by price ascending (default) - Add page_size to ensure pagination wrapper
        response = self.client.get(self.product_list_url + '?ordering=price&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        # Check that prices are in ascending order
        prices = [Decimal(p['price']) for p in data]
        self.assertEqual(prices, sorted(prices))

        # Order by price descending - Add page_size to ensure pagination wrapper
        response = self.client.get(self.product_list_url + '?ordering=-price&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        # Check that prices are in descending order
        prices = [Decimal(p['price']) for p in data]
        self.assertEqual(prices, sorted(prices, reverse=True))


    # --- API Tests (Product Detail) ---

    def test_product_detail_status_code_success(self):
        """Test that retrieving an existing product returns a 200 OK status code."""
        response = self.client.get(f'{self.product_list_url}{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_status_code_not_found(self):
        """Test that retrieving a non-existing product returns a 404 Not Found status code."""
        non_existing_id = Product.objects.count() + 1 # An ID that doesn't exist
        response = self.client.get(f'{self.product_list_url}{non_existing_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_detail_data(self):
        """Test that the data for a specific product is correct."""
        response = self.client.get(f'{self.product_list_url}{self.product3.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data['id'], self.product3.id)
        self.assertEqual(data['title'], 'Product C')
        self.assertEqual(data['price'], str(self.product3.price)) # Price comes as string from JSON
        self.assertEqual(data['category']['id'], self.category2.id) # Check nested category data


    # --- API Tests (Category List) ---

    def test_category_list_status_code(self):
        """Test that the category list endpoint returns a 200 OK status code."""
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_list_data(self):
        """Test that the category list endpoint returns all categories."""
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(len(data), 2) # Should return the 2 categories from setUp
        category_names = [item['name'] for item in data]
        self.assertIn('Category 1', category_names)
        self.assertIn('Category 2', category_names)
        # Check content of a specific category
        for item in data:
            if item['name'] == 'Category 1':
                self.assertEqual(item['description'], 'Description 1')

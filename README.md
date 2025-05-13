# Fake Commerce API

## Project Description

This is a public, read-only, fake e-commerce API designed to provide realistic product data (titles, prices, descriptions, images, categories, sizes, etc.) for junior developers and students to practice consuming REST APIs. It mimics the structure and behavior of a real e-commerce product catalog API.

Feel free to use this API in your frontend projects to display product lists, detail pages, practice filtering, pagination, and handling API responses.

## Built With

* Python 3.x
* Django
* Django REST Framework (DRF)
* PostgreSQL (as the database)
* Docker (for containerization)
* AWS (for deployment - details coming soon)

## Getting Started

**(Note: Detailed setup instructions will be added here later in the project development process.)**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Litti8/fake-commerce-api.git](https://github.com/Litti8/fake-commerce-api.git)
    cd fake-commerce-api
    ```
2.  **Set up the environment:**
    * Ensure you have Python 3.x and Git installed.
    * Create and activate a virtual environment (e.g., `python -m venv venv` then `source venv/bin/activate` or `.\venv\Scripts\activate`).
    * Install dependencies: `pip install -r requirements.txt`
    * **(More steps for database setup and environment variables will be added later)**

## API Endpoints

**(Note: Detailed API documentation (Swagger/OpenAPI) link will be provided here once deployed.)**

The API provides the following main endpoints:

* `GET /api/products/`: List all products with pagination and filtering options.
* `GET /api/products/{id}/`: Retrieve details for a specific product by ID.

## Contributing

This project is primarily for educational use. Contributions are not expected, but if you find issues or have suggestions, please open an issue on GitHub.

# 🚧 README Under Construction
In the meantime, feel free to check back later or explore the repository.

Thanks for your patience! 🙏

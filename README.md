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

Here are the basic steps to get the project running locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Litti8/fake-commerce-api.git](https://github.com/Litti8/fake-commerce-api.git)
    cd fake-commerce-api
    ```
2.  **Set up a Virtual Environment:**
    * Ensure you have Python 3.x and Git installed.
    * Create and activate a virtual environment:
        * Windows (CMD):
            ```bash
            python -m venv fake_commerce_env
            .\fake_commerce_env\Scripts\activate
            ```
        * macOS/Linux (Bash/Zsh):
            ```bash
            python3 -m venv fake_commerce_env
            source fake_commerce_env/bin/activate
            ```
        (Replace `fake_commerce_env` with your chosen environment name if different)

3.  **Install Dependencies:**
    * With your virtual environment activated, install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure Database:**
    * Ensure you have a PostgreSQL server running locally.
    * Create a database and a user for the project using `psql` or a GUI tool like pgAdmin. For example:
        ```sql
        -- Connect as a PostgreSQL superuser (e.g., postgres)
        CREATE DATABASE fake_commerce_db;
        CREATE USER myuser WITH PASSWORD 'mypassword';
        -- Connect specifically to the new database
        \c fake_commerce_db
        -- Grant privileges on the database itself (optional, but good practice)
        GRANT ALL PRIVILEGES ON DATABASE fake_commerce_db TO myuser;
        -- Grant privileges on the default public schema (crucial for migrations)
        GRANT CREATE ON SCHEMA public TO myuser;
        GRANT USAGE ON SCHEMA public TO myuser;
        -- Exit psql
        \q
        ```
        (Replace `fake_commerce_db`, `myuser`, and `mypassword` with your desired credentials)
    * Create a `.env` file in the project root directory (same level as `manage.py`) with your database credentials:
        ```dotenv
        # .env
        DB_NAME=your_db_name
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=localhost
        DB_PORT=5432
        ```
    * Add `/.env` to your `.gitignore` file to prevent committing sensitive data.

5.  **Run Migrations:**
    * Apply the database migrations to create the necessary tables:
        ```bash
        python manage.py migrate
        ```

6.  **Populate Database (Optional for development):**
    * You can populate the database with fake data using the included management command:
        ```bash
        python manage.py populate_products --num_products 200 # Adjust number as needed
        ```

## API Endpoints

The API provides the following main endpoints:

* `GET /api/products/`: List all products with pagination and filtering options.
* `GET /api/products/{id}/`: Retrieve details for a specific product by ID.

**(Note: Detailed API documentation (Swagger/OpenAPI) link will be provided here once deployed.)**

## Contributing

This project is primarily for educational use. Contributions are not expected, but if you find issues or have suggestions, please open an issue on GitHub.
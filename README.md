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
* Docker Compose (for multi-container management)
* Gunicorn (WSGI HTTP Server for production)
* AWS (for deployment - details coming soon)

## Getting Started

The recommended way to get this project running locally is using Docker Compose. This ensures a consistent environment including the application and the database.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Litti8/fake-commerce-api.git](https://github.com/Litti8/fake-commerce-api.git)
    cd fake-commerce-api
    ```

2.  **Ensure Docker is Installed:**
    * Make sure you have Docker Desktop (Windows/macOS) or the Docker Engine (Linux) installed and running.

3.  **Configure Environment Variables:**
    * Create a `.env` file in the project root directory (same level as `docker-compose.yml` and `manage.py`).
    * Define the database credentials that Docker Compose and your Django application will use. Ensure these match the configuration in `docker-compose.yml`.
    * Example `.env` file (replace with your desired values):
        ```dotenv
        # .env
        DB_NAME=fake_commerce_db
        DB_USER=myuser
        DB_PASSWORD=mypassword
        # When using Docker Compose, the host is the name of the DB service
        DB_HOST=db
        DB_PORT=5432
        # Django Secret Key (for development, can be simple)
        SECRET_KEY=your_django_secret_key
        # Set to 1 for debug mode (optional, but useful during development)
        DEBUG=1
        ```
    * **Important:** Add `/.env` to your `.gitignore` file to prevent committing sensitive data.

4.  **Build and Run with Docker Compose:**
    * From the project root directory, execute the following command to build the application image and start the database and web containers in detached mode (`-d`):
        ```bash
        docker-compose up -d --build
        ```
    * This will download the PostgreSQL image, build your application image based on the `Dockerfile`, create the Docker network and volume for the database, and start both containers. Wait a few moments for the database container to become healthy. You can check the status with `docker-compose ps`.

5.  **Run Migrations (inside Docker):**
    * Once the containers are up and the database service is healthy, apply the database migrations to create tables:
        ```bash
        docker-compose exec web python manage.py migrate
        ```

6.  **Populate Database (Optional, inside Docker):**
    * Populate the database with fake product data:
        ```bash
        docker-compose exec web python manage.py populate_products --num_products 200 # Adjust number as needed
        ```

7.  **Access the API:**
    * The Django application is served by **Gunicorn** inside the `web` container and is accessible via `http://localhost:8000/` on your host machine (due to port mapping in `docker-compose.yml`).
    * You can now access the API endpoints using your web browser or an API client like Postman:

---

**Alternative: Local Python/PostgreSQL Setup**

If you prefer to run the project directly using a local Python environment and a local PostgreSQL installation, follow these steps:

1.  **Clone the repository:** (Same as above)
    ```bash
    git clone [https://github.com/Litti8/fake-commerce-api.git](https://github.com/Litti8/fake-commerce-api.git)
    cd fake-commerce-api
    ```
2.  **Set up a Virtual Environment:** (Same as above)
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

3.  **Install Dependencies:** (Same as above)
    * With your virtual environment activated, install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure and Prepare Local Database:**
    * Ensure you have a PostgreSQL server running locally.
    * Create a database and a user for the project using `psql` or a GUI tool like pgAdmin. **Grant necessary privileges on the database AND the `public` schema to this user.** For example (replace values and connect as PostgreSQL superuser):
        ```sql
        CREATE DATABASE fake_commerce_db;
        CREATE USER myuser WITH PASSWORD 'mypassword';
        \c fake_commerce_db
        GRANT ALL PRIVILEGES ON DATABASE fake_commerce_db TO myuser; -- Optional but good practice
        GRANT CREATE ON SCHEMA public TO myuser; -- Crucial
        GRANT USAGE ON SCHEMA public TO myuser;   -- Crucial
        \q
        ```
    * Create a `.env` file in the project root directory (same level as `manage.py`). **For local setup, `DB_HOST` should be `localhost` or your DB server IP.**
        ```dotenv
        # .env
        DB_NAME=your_db_name
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=localhost # <-- Use localhost for local DB
        DB_PORT=5432
        SECRET_KEY=your_django_secret_key
        DEBUG=1
        ```
    * Add `/.env` to your `.gitignore` file.

5.  **Run Migrations (local venv):**
    * With your local venv activated, apply the database migrations:
        ```bash
        python manage.py migrate
        ```

6.  **Populate Database (Optional, local venv):**
    * Populate the database with fake product data:
        ```bash
        python manage.py populate_products --num_products 200 # Adjust number as needed
        ```

7.  **Run the Development Server (local venv):**
    * Start the Django development server:
        ```bash
        python manage.py runserver
        ```
    * Access the API endpoints via `http://127.0.0.1:8000/api/...`.

---

## API Endpoints

The API provides the following main endpoints, accessible at the root of the API (e.g., `http://localhost:8000/api/` when running locally):

* `GET /api/products/`: List all products. Supports pagination (`?page_size=`, `?page=`), filtering by category ID (`?category=`), search in title/description (`?search=`), and ordering by price/title (`?ordering=`, `?-ordering=`).
* `GET /api/products/{id}/`: Retrieve details for a specific product by its ID.
* `GET /api/categories/`: List all product categories.

**(Note: Detailed API documentation (Swagger/OpenAPI) link will be provided here once deployed.)**

## Contributing

This project is primarily for educational use. Contributions are not expected, but if you find issues or have suggestions, please open an issue on GitHub.
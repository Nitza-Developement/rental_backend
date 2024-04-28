# Rental Backend

This repository contains the implementation of a backend using Django REST Framework. It provides a solid foundation for building RESTful APIs with Django, enabling easy creation of web APIs following the REST principles.

## Features

- **Django Integration:** Built on top of Django, leveraging its robustness and scalability.
- **RESTful API:** Utilizes Django REST Framework to create RESTful APIs quickly and efficiently.
- **Authentication:** Supports various authentication methods including token-based authentication, session authentication, OAuth, etc.
- **Serialization:** Provides powerful serialization for converting complex data types, such as querysets and model instances, to native Python datatypes and vice versa.
- **Browsable API:** Offers a web-based API browser for easy exploration and testing of API endpoints.
- **Customizable:** Easily customizable and extendable according to project requirements.

## Setup

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```
   git clone https://github.com/Nitza-Developement/rental_backend
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

3. **Run migrations:**

   ```
   python manage.py migrate
   ```

4. **Create a superuser (optional):**

   ```
   python manage.py createsuperuser
   ```

5. **Start the development server:**

   ```
   python manage.py runserver
   ```

## Usage

Once the server is running, you can access the API endpoints using tools like `curl`, Postman, or any HTTP client. The API endpoints will be available at `http://localhost:8000/`.

To access the browsable API, navigate to `http://localhost:8000/api/` in your web browser. Here, you can explore the available endpoints, interact with them, and test the API.

## Configuration

- **Settings:** Modify the `settings.py` file to configure various aspects of the Django project including database settings, installed apps, middleware, etc.
- **URLs:** Define API endpoints and URL patterns in the `urls.py` file within the Django app.
- **Models:** Define database models in the `models.py` file within the Django app.
- **Views:** Create views to handle HTTP requests and responses in the `views.py` file within the Django app.
- **Serializers:** Define serializers to convert complex data types to native Python datatypes and vice versa in the `serializers.py` file within the Django app.

## Contributing Guidelines

1. **Include All Models in the Admin Site**: Ensure all models are registered in the Django admin site. Provide meaningful `__str__()` functions for each model to facilitate easy identification of instances in the admin interface.

2. **Use a Single App Called "rental"**: All functionalities in this repository should be contained within a single Django app named "rental".

3. **Code Formatting**: Utilize the Black code formatter with its default configuration for this project. Ensure your code adheres to the formatting standards before submitting a pull request.

4. **Include Tests for All Routes**: Write tests to cover all routes and functionalities implemented. Tests ensure the reliability and stability of the project.

5. **Organize Models in Separate Files**: Create a file within the `models` folder for each model. Name the files meaningfully, such as `my_module.py`, to improve code organization and maintainability.

## Submitting a Pull Request

1. Fork the repository to your GitHub account.

2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature-name
    ```

3. Make your changes and ensure they adhere to the contributing guidelines.

4. Commit your changes:
    ```bash
    git commit -m "Brief description of your changes"
    ```

5. Push your changes to your fork:
    ```bash
    git push origin feature-name
    ```

6. Open a pull request on the main repository's `develop` branch.

7. Provide a clear description of your changes in the pull request, including any relevant information or context.

8. Await review and feedback from project maintainers. Make any requested changes and updates as necessary.

9. Once approved, your changes will be merged into the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

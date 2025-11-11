# Laango Backend

A Django REST Framework backend for the Laango project.

## Change Log and Features in Progress:
- Twilio is set up. Need to accept incoming text messages and update job assignment and status.

## To Access Live Demo:
- Live demo is available [here](https://laango-app-ca0a792eac66.herokuapp.com/admin). Use sample_user and sample_password as the login credentials, which should grant you read-only access to view functionality.

## Features

- Django 5.2.8
- Django REST Framework for API development
- CORS headers support for frontend integration
- Environment-based configuration using python-decouple
- SQLite database (easily configurable to PostgreSQL/MySQL)

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd laango_backend
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and update the following variables:

- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names
- `CORS_ALLOWED_ORIGINS`: Add your frontend URLs

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Health Check

- **URL**: `/api/health/`
- **Method**: `GET`
- **Description**: Check if the API is running
- **Response**:

  ```json
  {
    "status": "ok",
    "message": "Laango API is running"
  }
  ```

### Admin Panel

- **URL**: `/admin/`
- **Description**: Django admin interface

## Project Structure

```text
laango_backend/
├── api/                    # Main API application
│   ├── views.py           # API views
│   ├── urls.py            # API URL routing
│   ├── models.py          # Database models
│   └── serializers.py     # DRF serializers
├── laango/                # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── .env.example          # Example environment file
```

## Development

### Adding a new app

```bash
python manage.py startapp app_name
```

Don't forget to add it to `INSTALLED_APPS` in [laango/settings.py](laango/settings.py)

### Creating migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running tests

```bash
python manage.py test
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed host names | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:5173` |

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Update `SECRET_KEY` with a strong secret key
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up a production database (PostgreSQL recommended)
5. Configure static files serving
6. Use a production WSGI server (gunicorn, uWSGI)
7. Set up HTTPS

## License

See [LICENSE](LICENSE) file for details.

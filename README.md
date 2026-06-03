# Kina Musica Backend

A Django REST API backend for the Kina Musica application, including user authentication, albums, songs, lyrics, and fan/artist features.

## Features

- JWT authentication with login, registration, password reset, and OTP flows
- Swagger UI documentation available at `/api/docs/`
- Redoc docs at `/api/redoc/`
- Local SQLite fallback database for development
- CORS enabled for all origins

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy or create `.env` with values for `SECRET_KEY` and optionally `DATABASE_URL`.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Documentation

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Notes

- The project currently uses a local SQLite DB when no `DATABASE_URL` is available.
- Do not use the development server in production.

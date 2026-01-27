# AIMailer Web Control Panel

A comprehensive SaaS platform for creating, managing, and distributing custom newsletters. Built with Django REST Framework and React.

## Features

- 🔐 **User Authentication** - Registration, login, 2FA with TOTP
- 📧 **Newsletter Management** - Create and manage multiple newsletters
- 📰 **RSS Integration** - Aggregate content from multiple RSS sources
- 👥 **Subscriber Management** - Import, export, and manage subscribers
- 🎨 **Public Discovery** - Browse and search newsletters by category
- 📊 **Analytics** - Track sends, opens, clicks, and subscriber growth
- ⏰ **Scheduled Sending** - Automated newsletter delivery
- 🔗 **One-Click Unsubscribe** - Token-based unsubscribe system

## Tech Stack

### Backend
- **Django 6.0** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Production database (SQLite for dev)
- **Celery** - Background task processing
- **Redis** - Cache and message broker
- **JWT** - Token-based authentication

### Frontend (Coming Soon)
- **React** - UI framework
- **React Router** - Navigation
- **Axios** - API client
- **Bootstrap/Material-UI** - UI components

## Project Structure

```
web/
├── config/              # Django project settings
├── accounts/            # User authentication and profiles
├── newsletters/         # Newsletter management
├── public/              # Public-facing API
├── integrations/        # AIMailer integration bridge
├── tasks/               # Celery background tasks
├── templates/           # Email templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploads
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🐳 Quick Start with Docker

The easiest way to run the web interface along with its dependencies (PostgreSQL, Redis, Celery) is using Docker Compose from the project root.

```bash
# From the project root (AIMailer/)
docker-compose up -d --build
```

See the [Root README](../README.md#%F0%9F%90%B3-quick-start-with-docker) for more details.

## 🚀 Manual Installation

### Prerequisites

- Python 3.12+
- Redis (for Celery)
- PostgreSQL (for production)

### Installation

1. **Navigate to the web directory:**
   ```bash
   cd web
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   You can use the standard Django command or the custom `reset_admin` command (recommended for email-based auth).

   > [!IMPORTANT]
   > If you are running the app in **Docker**, you must run these commands inside the container to update the PostgreSQL database. Running them in your local venv will only update a local SQLite file which the website does not use.

   **Inside Docker (recommended):**
   ```bash
   docker exec -it aimailer-web-1 python manage.py reset_admin <email> --password <password> --username <optional_username>
   ```

   **Local Development (SQLite only):**
   ```bash
   python manage.py reset_admin <email> --password <password> --username <optional_username>
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the admin panel:**
   Open http://localhost:8000/admin

## Development

### Running the Development Server

```bash
python manage.py runserver
```

### Running Celery Worker (for background tasks)

```bash
celery -A config worker -l info
```

### Running Celery Beat (for scheduled tasks)

```bash
celery -A config beat -l info
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests

```bash
python manage.py test
```

### Administrative Commands

#### `reset_admin`
Resets the password for an existing superuser or creates a new one with administrative privileges. This is specifically designed for the email-based `CustomUser` model.

**Docker command:**
```bash
docker exec -it aimailer-web-1 python manage.py reset_admin <email> --password <password> --username <optional_username>
```

**Local command:**
```bash
python manage.py reset_admin <email> --password <password> --username <optional_username>
```

### Newsletter Admin UI Enhancements

The Newsletter administration interface has been enhanced for better usability:

- **Keywords JSON Handling**: The standard JSON textarea has been replaced with a simple comma-separated text input. The system automatically converts this to and from the required JSON array format transparently.
- **Interactive Tooltips**: Field descriptions (help text) are now tucked behind blue eye icons (👁). Hover over these icons to see detailed information about each field.

These features are powered by custom static assets located in `web/static/newsletters/`.

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login (JWT)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/2fa/enable/` - Enable 2FA
- `POST /api/auth/2fa/verify/` - Verify 2FA code

### Newsletters
- `GET /api/newsletters/` - List user's newsletters
- `POST /api/newsletters/` - Create newsletter
- `GET /api/newsletters/{id}/` - Get newsletter details
- `PUT /api/newsletters/{id}/` - Update newsletter
- `DELETE /api/newsletters/{id}/` - Delete newsletter

### Public
- `GET /api/public/newsletters/` - Browse public newsletters
- `GET /api/public/newsletters/{slug}/` - Newsletter details
- `POST /api/public/subscribe/` - Subscribe to newsletter
- `GET /api/public/unsubscribe/{token}/` - Unsubscribe

## Database Models

### Accounts
- **CustomUser** - Extended user model with email verification and subscription tiers
- **UserProfile** - User profile information

### Newsletters
- **Category** - Newsletter categories
- **Newsletter** - Core newsletter entity
- **NewsletterConfig** - Newsletter configuration
- **RSSSource** - RSS feed sources
- **Subscriber** - Newsletter subscribers
- **SendHistory** - Track newsletter sends
- **EmailEvent** - Track email events (opens, clicks, bounces)

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DEBUG` - Debug mode (True/False)
- `SECRET_KEY` - Django secret key
- `DB_ENGINE` - Database engine
- `REDIS_URL` - Redis connection URL
- `EMAIL_BACKEND` - Email backend
- `CELERY_BROKER_URL` - Celery broker URL

## Next Steps

1. ✅ Django project setup
2. ✅ Database models
3. ⏳ Authentication endpoints (registration, login, 2FA)
4. ⏳ Newsletter CRUD API
5. ⏳ Celery tasks for newsletter sending
6. ⏳ React frontend
7. ⏳ Docker deployment

## Contributing

This is a private project. For questions or issues, contact the development team.

## License

Proprietary - All rights reserved

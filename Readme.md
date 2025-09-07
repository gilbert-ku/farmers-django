# 🌾 Farmer Management System API

A comprehensive Django REST API for managing agrovet businesses and their registered farmers. This system provides secure authentication, automated farmer registration, and dashboard management for agrovets and farmers.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🏪 Agrovet Management
- **Registration & Authentication**: Secure agrovet account creation with business details
- **Dashboard**: View registered farmers, business statistics, and management tools
- **Farmer Registration**: Register farmers with automatic credential generation

### 👨‍🌾 Farmer Management  
- **Automated Registration**: Agrovets can register farmers with name, email, and farm location
- **Secure Credentials**: Random password generation and email delivery
- **Mandatory Password Reset**: First-time login requires password change
- **Dashboard Access**: Personalized farmer dashboard after authentication

### 🔐 Security Features
- JWT-based authentication
- Secure password generation (12-character random passwords)
- Forced password reset on first login
- Email-only credential delivery (no SMS dependencies)
- User type-based access control
- CORS configuration for frontend integration

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API     │    │   Database      │
│   (Next.js)     │◄──►│   (REST API)     │◄──►│   (SQLite/      │
│                 │    │                  │    │    PostgreSQL)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Email Service  │
                       │   (SMTP)         │
                       └──────────────────┘
```

### Data Models

```
User (AbstractUser)
├── user_type: agrovet | farmer
├── email (unique)
├── must_reset_password
└── Standard user fields

Agrovet
├── user: OneToOne → User
├── business_name
├── registration_number
└── location

Farmer  
├── user: OneToOne → User
├── registered_by: ForeignKey → Agrovet
└── farm_location
```

## 🛠️ Tech Stack

### Backend
- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **JWT Authentication** - Token-based auth
- **SQLite/PostgreSQL** - Database
- **SMTP Email** - Credential delivery

### Frontend Integration
- **CORS Headers** - Cross-origin requests
- **JSON API** - RESTful endpoints
- **JWT Tokens** - Stateless authentication

### Development Tools
- **Python 3.10+**
- **Postman** - API testing
- **Virtual Environment** - Dependency management

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/farmer-management-api.git
cd farmer-management-api
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/farmer_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@example.com

# Frontend URL (for email links)
SITE_URL=http://localhost:3000

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Settings Configuration

Key settings in `settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'core.User'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

#### Register Agrovet
```http
POST /api/auth/register/agrovet/
Content-Type: application/json

{
    "email": "agrovet@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "business_name": "Green Valley Agrovets",
    "registration_number": "AGR-2024-001",
    "location": "Nairobi, Kenya"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "agrovet",
        "must_reset_password": false
    }
}
```

#### Reset Password
```http
POST /api/auth/password-reset/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "new_password": "NewSecurePass123!",
    "new_password2": "NewSecurePass123!"
}
```

### Agrovet Endpoints

#### Get Dashboard
```http
GET /api/agrovet/dashboard/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "agrovet": {
        "id": 1,
        "business_name": "Green Valley Agrovets",
        "registration_number": "AGR-2024-001",
        "location": "Nairobi, Kenya"
    },
    "farmers": [...],
    "total_farmers": 5
}
```

#### Register Farmer
```http
POST /api/agrovet/register-farmer/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Mary",
    "last_name": "Wanjiku", 
    "email": "mary@example.com",
    "farm_location": "Kiambu County, Kenya"
}
```

### Farmer Endpoints

#### Get Dashboard
```http
GET /api/farmer/dashboard/
Authorization: Bearer <access_token>
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Token Lifecycle
1. **Login** → Receive `access` and `refresh` tokens
2. **API Requests** → Include `access` token in Authorization header
3. **Token Expiry** → Use `refresh` token to get new `access` token
4. **Logout** → Client-side token removal

### Authorization Header Format
```
Authorization: Bearer <access_token>
```

### Token Refresh
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

## 💡 Usage Examples

### Frontend Integration (Next.js)

```javascript
// lib/api.js
class ApiService {
  constructor() {
    this.baseURL = 'http://localhost:8000/api';
  }

  async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    return response.json();
  }

  async loginUser(email, password) {
    const data = await this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }

  async registerFarmer(farmerData) {
    return this.request('/agrovet/register-farmer/', {
      method: 'POST',
      body: JSON.stringify(farmerData),
    });
  }
}

export default new ApiService();
```

### Python Client Example

```python
import requests

class FarmerAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = f"{base_url}/api"
        self.access_token = None
    
    def login(self, email, password):
        response = requests.post(f"{self.base_url}/auth/login/", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access"]
            return data
        return None
    
    def register_farmer(self, farmer_data):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(
            f"{self.base_url}/agrovet/register-farmer/", 
            json=farmer_data, 
            headers=headers
        )
        return response.json()

# Usage
client = FarmerAPIClient()
client.login("agrovet@example.com", "password123")
client.register_farmer({
    "first_name": "John",
    "last_name": "Farmer",
    "email": "john@example.com",
    "farm_location": "Nairobi"
})
```

## 🧪 Testing

### Unit Tests
```bash
python manage.py test
```

### API Testing with Postman

1. **Import Collection**: Import the provided Postman collection
2. **Set Environment**: Configure base URL and tokens
3. **Run Tests**: Execute requests in sequence

### Test Data Generation

```python
# test_data.py
python manage.py shell

from core.models import User, Agrovet, Farmer

# Create test agrovet
agrovet_user = User.objects.create_user(
    username='test@example.com',
    email='test@example.com', 
    password='testpass123',
    user_type='agrovet'
)

agrovet = Agrovet.objects.create(
    user=agrovet_user,
    business_name='Test Agrovet',
    registration_number='TEST-001',
    location='Test Location'
)
```

### Email Testing

For development, use console email backend:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will be printed to the Django console.

## 🚀 Deployment

### Production Settings

```python
# settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "farmer_project.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/farmer_db
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: farmer_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Heroku Deployment

```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
heroku config:set EMAIL_HOST_USER=your-email
heroku config:set EMAIL_HOST_PASSWORD=your-password

git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 📋 Requirements

```txt
# requirements.txt
Django>=4.2.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.2.0
django-cors-headers>=4.0.0
python-decouple>=3.6
psycopg2-binary>=2.9.0
gunicorn>=20.1.0
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 🐛 Troubleshooting

### Common Issues

#### Migration Errors
```bash
# Reset migrations (development only)
rm db.sqlite3
rm core/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

#### CORS Issues
```python
# settings.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

#### Email Not Sending
```python
# Use console backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### JWT Token Issues
```python
# Check token expiry settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

## 📞 Support

- **Documentation**: Check this README
- **Issues**: Create GitHub issues for bugs
- **Email**: support@yourproject.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Django REST Framework community
- JWT authentication libraries
- Contributors and testers

---

**Made with ❤️ for the farming community**
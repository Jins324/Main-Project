
# Kids Learning Tool

A Django application for managing children's learning activities with parent-child user relationships.

## Features

- Custom User model with Parent/Child roles
- Parent registration and login
- Child account management by parents
- Separate dashboards for parents and children
- Responsive HTML templates

## User Model

The application uses a custom User model (`CustomUser`) that extends Django's `AbstractUser`:

- **is_parent**: Boolean field to distinguish between parents and children
- **parent_account**: Foreign key linking children to their parent accounts

## URL Structure

- `/accounts/login/` - Login page
- `/accounts/register/` - Parent registration
- `/accounts/parent/dashboard/` - Parent dashboard (manage children)
- `/accounts/child/dashboard/` - Child dashboard (learning activities)
- `/accounts/parent/add-child/` - Add new child account
- `/admin/` - Django admin interface

## Getting Started

1. Install dependencies:
   ```bash
   pip install django
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://localhost:8000`

## Usage

1. **Parent Registration**: Visit `/accounts/register/` to create a parent account
2. **Login**: Use the login form to access your dashboard
3. **Add Children**: From the parent dashboard, add child accounts
4. **Child Access**: Children can log in with their credentials to access learning activities

## Default Admin Access

- Username: `admin`
- Password: `admin123`
- URL: `http://localhost:8000/admin/`

## Project Structure

```
kids_learning_tool/
├── kids_learning_tool/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                        # Core app
│   ├── models.py               # Custom User model
│   ├── views.py                # Authentication and dashboard views
│   ├── forms.py                # User registration forms
│   ├── urls.py                 # Core app URLs
│   ├── templates/core/         # HTML templates
│   └── ...
└── manage.py
```

## Next Steps

This is a basic setup. Future enhancements could include:

- Learning activities and games
- Progress tracking
- Parental controls
- Content management system
- User profiles and settings

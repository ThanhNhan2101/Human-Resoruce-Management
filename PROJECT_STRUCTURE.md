# 📋 HRM System - Project Structure Documentation

## 🏗️ Cấu Trúc Project

```
hrm_project/
│
├── config/                        # Django configuration
│   ├── __init__.py
│   ├── asgi.py                   # ASGI config
│   ├── wsgi.py                   # WSGI config
│   ├── urls.py                   # Main URL config
│   ├── forms.py                  # Custom LoginForm (Vietnamese messages)
│   └── settings/
│       ├── __init__.py
│       └── base.py               # Base settings
│
├── core/                          # Core business logic
│   │
│   ├── employees/                 # Employee management module
│   │   ├── __init__.py
│   │   ├── admin.py              # Admin interface
│   │   ├── apps.py               # App configuration
│   │   ├── urls.py               # URL routing
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── employee.py       # Employee, Department models
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   └── employee_views.py # Views for employee management
│   │   ├── templates/employees/  # HTML templates
│   │   │   ├── employee_list.html
│   │   │   ├── employee_detail.html
│   │   │   ├── employee_form.html
│   │   │   ├── employee_confirm_delete.html
│   │   │   ├── department_list.html
│   │   │   └── department_form.html
│   │   ├── usecase/              # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   └── employee_services.py
│   │   │   └── selectors/
│   │   │       ├── __init__.py
│   │   │       └── employee_selectors.py
│   │   └── migrations/           # Database migrations
│   │
│   ├── leaves/                    # Leave management module
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── leave.py          # Leave model
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   └── leave_views.py    # Leave request views
│   │   ├── templates/leaves/
│   │   │   ├── leave_list.html
│   │   │   ├── leave_detail.html
│   │   │   ├── leave_form.html
│   │   │   └── leave_confirm_delete.html
│   │   ├── usecase/
│   │   │   ├── __init__.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   └── leave_services.py
│   │   │   └── selectors/
│   │   │       ├── __init__.py
│   │   │       └── leave_selectors.py
│   │   └── migrations/
│   │
│   └── attendance/                # Attendance management module
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── urls.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── attendance.py      # Attendance model
│       ├── views/
│       │   ├── __init__.py
│       │   └── attendance_views.py # Attendance views
│       ├── templates/attendance/
│       │   ├── attendance_list.html
│       │   ├── attendance_detail.html
│       │   ├── attendance_form.html
│       │   └── daily_attendance.html
│       └── migrations/
│
├── common/                        # Shared utilities
│   ├── __init__.py
│   └── base_model.py             # Abstract base models
│
├── templates/                     # Global templates
│   ├── base.html                 # Main layout template (dark sidebar)
│   ├── dashboard.html            # Dashboard with stat cards
│   ├── index.html                # Home redirect
│   └── auth/
│       ├── auth_base.html        # Auth page base (dark gradient)
│       └── login.html            # Login page
│
├── static/                        # Static files
│   ├── css/
│   │   └── main.css              # Complete design system (CSS variables, components)
│   └── js/
│
├── scripts/                       # Utility scripts
│   └── seed_data.py              # Demo data seeder
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database (dev)
├── README.md                      # Project documentation
├── PROJECT_STRUCTURE.md          # This file
├── QUICKSTART.md                 # Quick start guide
```

## 📦 Key Files

### config/forms.py

Custom LoginForm with Vietnamese error messages, properly sets `self.user_cache` for Django 5+ login flow.

### config/urls.py

Main URL router with:

- Login view using custom LoginForm
- Logout view with POST-only redirect
- Employee, Leave, and Attendance app URLs

### static/css/main.css

Complete design system with:

- CSS custom properties (variables)
- Responsive dark sidebar
- Component styles (buttons, forms, tables, cards)
- Utility classes

### scripts/seed_data.py

Creates demo data:

- 12 employees across 5 departments
- 12 leave requests (various statuses)
- 360 attendance records (30 days × 12 employees)
- Admin superuser (admin / admin123)

│ └── seed_data.py # Demo data generator
│
├── manage.py # Django management script
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── README.md # Project documentation
├── QUICKSTART.md # Quick start guide
└── PROJECT_STRUCTURE.md # This file

```

## 🔄 Design Patterns Used

### 1. **Service/Selector Pattern (Usecase Layer)**

```

Separation of concerns:

- Selectors: Query database (READ operations)
- Services: Business logic (WRITE/UPDATE operations)

Example:
core/employees/usecase/
├── selectors/employee_selectors.py # get_employee_by_id(), search_employees()
└── services/employee_services.py # create_employee(), update_employee()

```

### 2. **Django MVT (Model-View-Template)**

```

- Models: Database schema
- Views: Business logic + request handling
- Templates: HTML rendering

```

### 3. **Class-Based Views**

```

Using Django's generic views:

- ListView: Display list of objects
- DetailView: Display single object
- CreateView: Create new object
- UpdateView: Update object
- DeleteView: Delete object

```

## 📊 Entity Relationship

```

Employee
├── department (ForeignKey to Department)
├── position (ForeignKey to Position)
├── attendances (OneToMany)
└── leaves (OneToMany)

Department
├── employees (OneToMany)
└── positions (OneToMany)

Position
└── employees (OneToMany)

Leave
├── employee (ForeignKey to Employee)
├── leave_type (ForeignKey to LeaveType)
└── approved_by (ForeignKey to Employee - manager)

LeaveType
└── leaves (OneToMany)

Attendance
└── employee (ForeignKey to Employee)

```

## 🔌 URL Routing

### Main URL Dispatcher

```

config/urls.py (Root)
├── /admin/ Admin panel
├── /accounts/login Django auth login
├── /accounts/logout Django auth logout
└── /dashboard/ Employee app URLs
├── employees/ Employees
├── departments/ Departments
└── ...
├── /leaves/ Leaves app URLs
└── /attendance/ Attendance app URLs

```

## 🎨 UI/UX Stack

### Frontend Technologies

- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Jinja2**: Django template engine
- **CSS3**: Custom styling

### Key UI Components

```

- Navbar: Navigation and user info
- Sidebar: Main menu navigation
- Cards: Content containers
- Tables: Data display
- Forms: Input handling
- Modals: Dialogs
- Badges: Status indicators
- Alerts: Notifications

```

## 🗄️ Database

### Default: SQLite

- File: `db.sqlite3`
- Perfect for development
- Created automatically by Django

### Production: PostgreSQL

- Edit `.env` file:
```

DB_ENGINE=django.db.backends.postgresql
DB_NAME=hrm_db
DB_USER=hrm_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

```

## 📦 Dependencies

```

Django==5.2 # Web framework
django-environ==0.12.0 # Environment variables
Pillow==10.0.0 # Image processing
psycopg2-binary==2.9.10 # PostgreSQL adapter (optional)
python-dotenv==1.1.1 # .env file support

````

## 🔒 Authentication & Authorization

### Current Implementation

- Django built-in authentication
- Username/Password login
- Session-based authentication
- Template-level permission checks

### Future Enhancement

```python
# Could add:
- Django REST Framework + JWT
- OAuth2 integration
- Social login (Google, Facebook)
- Two-factor authentication
- Role-based access control (RBAC)
````

## 🚀 Running the Project

### Development

```bash
python manage.py runserver
# Access at http://localhost:8000
```

### Production

```bash
# Collect static files
python manage.py collectstatic

# Use gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Use with Nginx for reverse proxy
# Use with Systemd for auto-restart
```

## 📝 Database Migrations

### View migrations

```bash
python manage.py showmigrations
```

### Create new migration

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Rollback migration

```bash
python manage.py migrate core 0001
```

## 🧪 Testing Structure (To be implemented)

```
tests/
├── __init__.py
├── accounts/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_services.py
├── employees/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_services.py
└── conftest.py  # Pytest fixtures
```

## 🔍 Code Organization Best Practices

### In This Project

✅ Separation of concerns (Services, Selectors, Views)
✅ DRY (Don't Repeat Yourself)
✅ Clear naming conventions
✅ Modular structure
✅ Template inheritance
✅ Static file organization
✅ Environment-based configuration

### To Implement

- [ ] Comprehensive test coverage
- [ ] API layer with DRF
- [ ] Logging system
- [ ] Error handling middleware
- [ ] Performance caching
- [ ] Background task queue (Celery)
- [ ] Documentation via Swagger/OpenAPI

## 🔐 Security Considerations

### Implemented

- CSRF protection (Django default)
- SQL injection prevention (ORM)
- XSS prevention (Template escaping)
- Secure password hashing


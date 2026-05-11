# Copilot instructions for this repository

Purpose
- Provide concise, repo-specific instructions so Copilot sessions are effective and reproducible.

Quick setup / build / run
- Create venv (Windows): python -m venv venv && venv\Scripts\activate
- Install: pip install -r requirements.txt
- Apply migrations: python manage.py migrate
- Seed demo data: python scripts/seed_data.py
- Run dev server: python manage.py runserver

Docker
- Build & run: docker-compose up -d --build
- Exec into web container: docker-compose exec web bash
- Run Django commands inside container: docker-compose exec web python manage.py <command>

Tests
- Test runner: pytest (pytest.ini present)
- Django settings for tests: DJANGO_SETTINGS_MODULE=config.settings.base
- Run full suite: pytest
- Run a single test (examples):
  - pytest tests/test_employees.py::TestEmployee::test_create_employee
  - pytest tests -k "employee and create"
- Run tests inside Docker: docker-compose exec web pytest

Linting / Formatting
- No project-wide linter or formatter configured. Add tools (black/flake8/isort) if desired and document commands here.

High-level architecture (big picture)
- Django 5.2 project with config/ (ASGI/WSGI, settings/base.py, custom LoginForm).
- core/ contains feature apps: employees/, leaves/, attendance/.
- Each app follows a "usecase" layering: selectors/ (read queries) and services/ (business logic / write operations).
- common/ contains shared base models (base_model.py).
- Templates live under templates/; a dark-sidebar layout is used.
- Static assets in static/ (css main.css holds design system).
- scripts/seed_data.py seeds demo data (admin + employees, leaves, attendance).
- Docker compose defines web (Daphne/Gunicorn), db (Postgres), redis (Channels layer) for production-like local runs.
- Tests live under tests/ and use pytest-django.

Key conventions & patterns (repo-specific)
- Usecase layer: keep read-only DB queries in selectors/ and side-effecting business logic in services/.
- Views prefer Django class-based generic views (ListView/DetailView/CreateView/etc.).
- Login uses a custom LoginForm (config/forms.py) and logout is POST-only.
- Status fields (Employee/Leave/Attendance) use uppercase string constants (e.g., PENDING / APPROVED / REJECTED).
- Seeds: scripts/seed_data.py is the canonical demo-data generator — use it for local realistic data.
- Tests: pytest.ini sets DJANGO_SETTINGS_MODULE=config.settings.base; run tests from project root.

Tests & CI hints for Copilot
- Respect pytest.ini test discovery patterns (python_files = tests.py test_*.py *_tests.py).
- Use -k or explicit node::class::test to scope runs when proposing or running changes.

Files to consult for more details
- README.md, QUICKSTART.md, PROJECT_STRUCTURE.md, DOCKER_GUIDE.md

Notes for future Copilot sessions
- Prefer the usecase/services+selectors pattern when suggesting refactors or moving business logic.
- When proposing DB queries, follow selectors/ style and avoid introducing side effects there.
- Keep login/logout behavior and CSRF rules intact (logout must be POST).

--
Created from repository documentation (README.md, QUICKSTART.md, PROJECT_STRUCTURE.md, DOCKER_GUIDE.md, pytest.ini).

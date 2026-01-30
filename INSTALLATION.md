# Installation Guide - Personal Finance Tracker

## Quick Start (Windows)

### Prerequisites
- Python 3.11 or higher
- pip (comes with Python)
- Git (optional)

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\iniro\Desktop\Vizja Projects\Diploma Project"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Start Development Server
```bash
python manage.py runserver
```

### Step 8: Access Application
Open your browser and navigate to:
- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Quick Start (Linux/macOS)

### Step 1: Navigate to Project Directory
```bash
cd ~/Desktop/Vizja\ Projects/Diploma\ Project
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 4-8: Same as Windows steps above

## Troubleshooting

### Issue: "python: command not found"
**Solution**: Use `python3` instead of `python`

### Issue: Port 8000 already in use
**Solution**: Run on a different port:
```bash
python manage.py runserver 8001
```

### Issue: Database errors
**Solution**: Reset the database:
```bash
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading
**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

## Automated Setup (Windows)

Run the provided setup script:
```bash
setup.bat
```

Or use the quick start script:
```bash
run_server.bat
```

## Testing

Run the test suite:
```bash
python manage.py test
```

Run specific test:
```bash
python manage.py test tracker.tests.TransactionTestCase
```

## Default Test User

After running migrations, you can create a test user:
```bash
python manage.py shell
```

Then in the Python shell:
```python
from django.contrib.auth.models import User
User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
```

## Production Deployment

See README.md for production deployment instructions using Gunicorn and PostgreSQL.

# Deployment Guide - Personal Finance Tracker

## Production Deployment

### Prerequisites
- Python 3.11+
- PostgreSQL 12+ (recommended for production)
- Nginx or Apache (web server)
- Gunicorn (WSGI application server)
- Supervisor or systemd (process manager)

### Step 1: Prepare Server

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install Python and dependencies
sudo apt-get install python3.11 python3-pip python3-venv postgresql postgresql-contrib nginx

# Create application user
sudo useradd -m -s /bin/bash financeapp
sudo su - financeapp
```

### Step 2: Clone and Setup Application

```bash
# Clone repository
git clone <repository-url> finance-tracker
cd finance-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Database

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE finance_tracker;
CREATE USER finance_user WITH PASSWORD 'secure_password';
ALTER ROLE finance_user SET client_encoding TO 'utf8';
ALTER ROLE finance_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE finance_user SET default_transaction_deferrable TO on;
ALTER ROLE finance_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE finance_tracker TO finance_user;
\q
```

### Step 4: Update Django Settings

Edit `finance_tracker/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finance_tracker',
        'USER': 'finance_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = 'your-secret-key-here'  # Generate a new one!

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

### Step 5: Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 6: Configure Gunicorn

Create `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

### Step 7: Setup Supervisor

Create `/etc/supervisor/conf.d/finance-tracker.conf`:

```ini
[program:finance-tracker]
directory=/home/financeapp/finance-tracker
command=/home/financeapp/finance-tracker/venv/bin/gunicorn -c gunicorn_config.py finance_tracker.wsgi:application
user=financeapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/finance-tracker/gunicorn.log
```

```bash
sudo mkdir -p /var/log/finance-tracker
sudo chown financeapp:financeapp /var/log/finance-tracker
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start finance-tracker
```

### Step 8: Configure Nginx

Create `/etc/nginx/sites-available/finance-tracker`:

```nginx
upstream finance_tracker {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /home/financeapp/finance-tracker/staticfiles/;
    }
    
    location /media/ {
        alias /home/financeapp/finance-tracker/media/;
    }
    
    location / {
        proxy_pass http://finance_tracker;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/finance-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 10: Setup Backups

Create backup script `/home/financeapp/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/financeapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U finance_user finance_tracker | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/financeapp/finance-tracker/media/

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

```bash
chmod +x /home/financeapp/backup.sh
# Add to crontab
crontab -e
# Add: 0 2 * * * /home/financeapp/backup.sh
```

### Monitoring and Maintenance

```bash
# Check application status
sudo supervisorctl status finance-tracker

# View logs
tail -f /var/log/finance-tracker/gunicorn.log

# Restart application
sudo supervisorctl restart finance-tracker

# Check Nginx status
sudo systemctl status nginx
```

## Docker Deployment (Alternative)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "-b", "0.0.0.0:8000", "finance_tracker.wsgi:application"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: finance_tracker
      POSTGRES_USER: finance_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn -b 0.0.0.0:8000 finance_tracker.wsgi:application
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      DATABASE_URL: postgresql://finance_user:secure_password@db:5432/finance_tracker
    depends_on:
      - db

volumes:
  postgres_data:
```

```bash
docker-compose up -d
```

## Troubleshooting

### Application won't start
```bash
sudo supervisorctl tail finance-tracker
```

### Database connection errors
```bash
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity WHERE datname = 'finance_tracker';"
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart nginx
```

### High memory usage
Adjust Gunicorn workers in `gunicorn_config.py`

### SSL certificate issues
```bash
sudo certbot renew --dry-run
sudo certbot renew
```

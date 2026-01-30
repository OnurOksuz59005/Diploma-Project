# Architecture Documentation - Personal Finance Tracker

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer (Frontend)                  │
│  HTML5 | CSS3 | JavaScript | Bootstrap 5 | Chart.js | Axios │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Web Server (Nginx/Apache)                   │
│              Static Files | Reverse Proxy                    │
└────────────────────────┬────────────────────────────────────┘
                         │ WSGI
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Server (Gunicorn)                   │
│                   Django Framework                           │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  REST API    │  │  Templates   │  │  Middleware  │
│  Endpoints   │  │  Rendering   │  │  & Auth      │
└──────────────┘  └──────────────┘  └──────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  Views | Serializers | Permissions | Validators             │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Transaction  │  │   Budget     │  │ Budget Alert │
│   Manager    │  │   Manager    │  │   Manager    │
└──────────────┘  └──────────────┘  └──────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer (ORM)                   │
│              Django ORM | QuerySet | Models                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Database Layer                             │
│  SQLite (Dev) | PostgreSQL (Prod) | Migrations              │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
Diploma Project/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
├── INSTALLATION.md                    # Installation guide
├── DEPLOYMENT.md                      # Deployment guide
├── FEATURES.md                        # Features documentation
├── ARCHITECTURE.md                    # This file
│
├── finance_tracker/                   # Main Django project
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI application
│
├── tracker/                           # Main application
│   ├── migrations/                    # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py                       # Django admin configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # Database models
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # API views
│   ├── urls.py                        # API URL routing
│   ├── frontend_urls.py               # Frontend URL routing
│   ├── auth_views.py                  # Authentication views
│   ├── forms.py                       # Django forms
│   ├── utils.py                       # Utility functions
│   ├── middleware.py                  # Custom middleware
│   ├── permissions.py                 # Custom permissions
│   ├── tests.py                       # Unit tests
│
├── templates/                         # HTML templates
│   ├── base.html                      # Base template
│   ├── index.html                     # Home page
│   ├── login.html                     # Login page
│   ├── register.html                  # Registration page
│   ├── dashboard.html                 # Dashboard
│   ├── transactions.html              # Transactions page
│   ├── budgets.html                   # Budgets page
│
├── static/                            # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   ├── images/
│
├── .gitignore                         # Git ignore rules
├── setup.sh                           # Linux setup script
├── setup.bat                          # Windows setup script
└── run_server.bat                     # Windows run script
```

## Data Flow

### Transaction Creation Flow
```
User Input (Frontend)
    ↓
JavaScript Form Submission
    ↓
POST /api/transactions/
    ↓
TransactionViewSet.create()
    ↓
TransactionSerializer.validate()
    ↓
Transaction Model.save()
    ↓
_check_budget_alerts()
    ↓
BudgetAlert.get_or_create()
    ↓
Response to Frontend
    ↓
Update UI
```

### Budget Alert Generation Flow
```
Transaction Created/Updated
    ↓
_check_budget_alerts() triggered
    ↓
Get Budget for category/month/year
    ↓
Calculate total spent
    ↓
Calculate percentage
    ↓
If percentage >= 90%
    → Create CRITICAL alert
Else if percentage >= 75%
    → Create WARNING alert
    ↓
Alert saved to database
    ↓
Frontend fetches alerts
    ↓
Display to user
```

### Dashboard Update Flow
```
Page Load / Auto-refresh (30s)
    ↓
GET /api/dashboard/stats/
    ↓
Calculate monthly totals
    ↓
GET /api/dashboard/chart_data/
    ↓
Get expense breakdown by category
    ↓
GET /api/alerts/unread/
    ↓
Fetch unread alerts
    ↓
GET /api/transactions/
    ↓
Fetch recent transactions
    ↓
Combine all data
    ↓
Return JSON response
    ↓
JavaScript updates DOM
    ↓
Chart.js renders charts
```

## Authentication Flow

```
User Registration
    ↓
POST /api/auth/register/
    ↓
Validate input
    ↓
Check username/email uniqueness
    ↓
Hash password
    ↓
Create User object
    ↓
Return user data
    ↓
Redirect to login

User Login
    ↓
POST /api/auth/login/
    ↓
Authenticate credentials
    ↓
Create session
    ↓
Return user data
    ↓
Store session cookie
    ↓
Redirect to dashboard

Protected Endpoints
    ↓
Check session/token
    ↓
Verify user identity
    ↓
Check permissions
    ↓
Process request
    ↓
Return data
```

## Database Schema

### Transaction Table
```sql
CREATE TABLE tracker_transaction (
    id BIGINT PRIMARY KEY,
    user_id INT FOREIGN KEY,
    type VARCHAR(10),
    category VARCHAR(20),
    amount DECIMAL(10, 2),
    description VARCHAR(255),
    date DATE,
    created_at DATETIME,
    updated_at DATETIME,
    INDEX (user_id, date),
    INDEX (user_id, type)
);
```

### Budget Table
```sql
CREATE TABLE tracker_budget (
    id BIGINT PRIMARY KEY,
    user_id INT FOREIGN KEY,
    category VARCHAR(20),
    limit DECIMAL(10, 2),
    month INT,
    year INT,
    created_at DATETIME,
    updated_at DATETIME,
    UNIQUE (user_id, category, month, year)
);
```

### BudgetAlert Table
```sql
CREATE TABLE tracker_budgetalert (
    id BIGINT PRIMARY KEY,
    user_id INT FOREIGN KEY,
    budget_id BIGINT FOREIGN KEY,
    alert_type VARCHAR(10),
    spent_amount DECIMAL(10, 2),
    percentage DECIMAL(5, 2),
    is_read BOOLEAN,
    created_at DATETIME
);
```

## API Architecture

### REST Endpoints Pattern
```
/api/transactions/              → List, Create
/api/transactions/{id}/         → Retrieve, Update, Delete
/api/transactions/by_category/  → Filter by category
/api/transactions/monthly_summary/ → Get monthly stats

/api/budgets/                   → List, Create
/api/budgets/{id}/              → Retrieve, Update, Delete
/api/budgets/current_month/     → Get current month budgets

/api/alerts/                    → List
/api/alerts/unread/             → Get unread alerts
/api/alerts/mark_as_read/       → Mark alert as read

/api/dashboard/stats/           → Get dashboard statistics
/api/dashboard/chart_data/      → Get chart data

/api/auth/login/                → User login
/api/auth/logout/               → User logout
/api/auth/register/             → User registration
/api/auth/profile/              → Get user profile
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         HTTPS/TLS Encryption            │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│      CSRF Token Validation              │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│    Session Authentication               │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│    Permission Checks                    │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│    Input Validation & Sanitization      │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│    Database Query Execution             │
└─────────────────────────────────────────┘
```

## Performance Optimization

### Database Optimization
- Indexes on frequently queried fields (user_id, date, type)
- Query optimization with select_related() and prefetch_related()
- Aggregation queries for statistics
- Connection pooling in production

### Frontend Optimization
- Minified CSS and JavaScript
- Lazy loading of images
- Caching of static assets
- Async API calls to prevent blocking
- Chart.js for efficient rendering

### Caching Strategy
- Template caching
- Query result caching
- Static file caching (browser)
- API response caching (where applicable)

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- Session storage in database/cache
- Load balancing with Nginx
- Multiple Gunicorn workers

### Vertical Scaling
- Database optimization
- Query optimization
- Caching layer (Redis)
- CDN for static files

### Database Scaling
- Read replicas for reporting
- Connection pooling
- Query optimization
- Partitioning for large tables

## Monitoring & Logging

### Application Monitoring
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Application logs
- User activity logs

### System Monitoring
- Server CPU/Memory usage
- Disk space
- Network bandwidth
- Database performance

### Alerting
- Error rate thresholds
- Response time thresholds
- Database connection pool exhaustion
- Disk space warnings

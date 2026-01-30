# Testing Guide - Personal Finance Tracker

## Unit Tests

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test tracker

# Run specific test class
python manage.py test tracker.tests.TransactionTestCase

# Run specific test method
python manage.py test tracker.tests.TransactionTestCase.test_create_transaction

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Cases

#### Transaction Tests
- `test_create_transaction`: Verify transaction creation
- `test_get_transactions`: Verify transaction retrieval
- `test_update_transaction`: Verify transaction updates
- `test_delete_transaction`: Verify transaction deletion
- `test_transaction_filtering`: Verify category filtering
- `test_monthly_summary`: Verify monthly calculations

#### Budget Tests
- `test_create_budget`: Verify budget creation
- `test_get_budgets`: Verify budget retrieval
- `test_budget_alert_on_high_spending`: Verify alert generation
- `test_budget_calculation`: Verify budget calculations

#### Dashboard Tests
- `test_dashboard_stats`: Verify statistics calculation
- `test_chart_data`: Verify chart data generation

#### Authentication Tests
- `test_user_registration`: Verify user registration
- `test_user_login`: Verify user login
- `test_user_logout`: Verify user logout
- `test_invalid_credentials`: Verify invalid login handling

## Integration Tests

### API Testing with cURL

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  -c cookies.txt

# Create transaction
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"type":"expense","category":"food","amount":25.50,"date":"2024-01-15","description":"Lunch"}'

# Get transactions
curl -X GET http://localhost:8000/api/transactions/ \
  -b cookies.txt

# Create budget
curl -X POST http://localhost:8000/api/budgets/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"category":"food","limit":500.00,"month":1,"year":2024}'

# Get dashboard stats
curl -X GET http://localhost:8000/api/dashboard/stats/ \
  -b cookies.txt
```

### API Testing with Postman

1. Import collection from API documentation
2. Set base URL: `http://localhost:8000/api`
3. Create environment variables for auth tokens
4. Run test suite

## Manual Testing Checklist

### User Registration & Authentication
- [ ] Register new user with valid credentials
- [ ] Register with duplicate username (should fail)
- [ ] Register with invalid email (should fail)
- [ ] Login with correct credentials
- [ ] Login with incorrect password (should fail)
- [ ] Logout successfully
- [ ] Access protected pages without login (should redirect)

### Transaction Management
- [ ] Create income transaction
- [ ] Create expense transaction
- [ ] View all transactions
- [ ] Filter transactions by category
- [ ] Edit existing transaction
- [ ] Delete transaction
- [ ] View transaction history
- [ ] Search transactions by description

### Budget Management
- [ ] Create budget for category
- [ ] View current month budgets
- [ ] Edit budget limit
- [ ] Delete budget
- [ ] Create duplicate budget (should fail)
- [ ] View budget progress bar

### Budget Alerts
- [ ] Create transaction that triggers 75% alert
- [ ] Create transaction that triggers 90% alert
- [ ] View unread alerts
- [ ] Mark alert as read
- [ ] Alert disappears after reading

### Dashboard
- [ ] View income total
- [ ] View expense total
- [ ] View balance calculation
- [ ] View expense chart
- [ ] View recent transactions
- [ ] View recent alerts
- [ ] Dashboard auto-refreshes

### UI/UX Testing
- [ ] Responsive design on mobile
- [ ] Responsive design on tablet
- [ ] Responsive design on desktop
- [ ] All buttons are clickable
- [ ] Form validation messages appear
- [ ] Loading indicators display
- [ ] Error messages are clear
- [ ] Success messages appear

### Performance Testing
- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms
- [ ] Dashboard updates smoothly
- [ ] Charts render without lag
- [ ] No console errors
- [ ] No memory leaks

### Security Testing
- [ ] CSRF token validation works
- [ ] Users can't access other users' data
- [ ] Password is hashed in database
- [ ] Session expires after logout
- [ ] SQL injection attempts fail
- [ ] XSS attempts fail

## Load Testing

### Using Apache Bench

```bash
# Install Apache Bench
# Windows: Download from Apache website
# Linux: sudo apt-get install apache2-utils

# Test dashboard endpoint
ab -n 1000 -c 10 http://localhost:8000/dashboard/

# Test API endpoint
ab -n 1000 -c 10 http://localhost:8000/api/transactions/
```

### Using Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class FinanceTrackerUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def view_dashboard(self):
        self.client.get("/dashboard/")
    
    @task
    def view_transactions(self):
        self.client.get("/api/transactions/")
    
    @task
    def view_budgets(self):
        self.client.get("/api/budgets/")
```

```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Browser Testing

### Chrome DevTools
- Open DevTools (F12)
- Check Console for errors
- Check Network tab for slow requests
- Check Performance tab for rendering issues
- Check Application tab for storage

### Firefox Developer Tools
- Similar to Chrome DevTools
- Additional CSS Grid inspector
- Network analysis tools

## Accessibility Testing

```bash
# Install axe DevTools browser extension
# Run automated accessibility checks
# Check keyboard navigation
# Test with screen reader
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Run coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report
```

## Test Data

### Creating Test Fixtures

```bash
# Create fixture
python manage.py dumpdata tracker > fixtures/test_data.json

# Load fixture
python manage.py loaddata fixtures/test_data.json
```

### Sample Test Data SQL

```sql
-- Insert test user
INSERT INTO auth_user (username, email, password) 
VALUES ('testuser', 'test@example.com', 'hashed_password');

-- Insert test transactions
INSERT INTO tracker_transaction (user_id, type, category, amount, date)
VALUES (1, 'income', 'salary', 3000.00, '2024-01-01');

INSERT INTO tracker_transaction (user_id, type, category, amount, date)
VALUES (1, 'expense', 'food', 50.00, '2024-01-15');

-- Insert test budget
INSERT INTO tracker_budget (user_id, category, limit, month, year)
VALUES (1, 'food', 500.00, 1, 2024);
```

## Debugging

### Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

Add to `settings.py`:

```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Test Report Template

```
Test Report - Personal Finance Tracker
Date: YYYY-MM-DD
Tester: Name
Build: Version

SUMMARY
- Total Tests: X
- Passed: X
- Failed: X
- Skipped: X
- Pass Rate: X%

DETAILED RESULTS
[List test results]

ISSUES FOUND
[List any bugs or issues]

RECOMMENDATIONS
[List recommendations]

SIGN-OFF
Tester: ___________
Date: ___________
```

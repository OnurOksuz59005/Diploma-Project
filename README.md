# Personal Finance Tracker with Smart Budgeting Suggestions

A comprehensive web application for personal finance management with intelligent budgeting recommendations, built with Django and modern frontend technologies.

## Features

### Core Functionality
- **User Authentication**: Secure registration and login system with password hashing
- **Transaction Management**: Log income and expense transactions with categories, amounts, and descriptions
- **Budget Management**: Set monthly budgets for different spending categories
- **Smart Budget Alerts**: Automatic alerts when spending reaches 75% (warning) or 90% (critical) of budget limit
- **Financial Dashboard**: Real-time overview of income, expenses, and balance
- **Data Visualization**: Interactive charts showing expense breakdown by category

### Technology Stack
- **Backend**: Python 3.11, Django 4.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Visualization**: Chart.js
- **HTTP Client**: Axios

## Project Structure

```
Diploma Project/
├── manage.py
├── requirements.txt
├── README.md
├── finance_tracker/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── tracker/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── frontend_urls.py
│   └── tests.py
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── transactions.html
    └── budgets.html
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Steps

1. **Clone/Navigate to project directory**
```bash
cd "c:\Users\iniro\Desktop\Vizja Projects\Diploma Project"
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional, for admin panel)**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Open browser and go to `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/users/register/` - User registration

### Transactions
- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create new transaction
- `GET /api/transactions/{id}/` - Get transaction details
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/by_category/` - Filter by category
- `GET /api/transactions/monthly_summary/` - Monthly summary

### Budgets
- `GET /api/budgets/` - List all budgets
- `POST /api/budgets/` - Create new budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `GET /api/budgets/current_month/` - Get current month budgets

### Budget Alerts
- `GET /api/alerts/` - List all alerts
- `GET /api/alerts/unread/` - List unread alerts
- `POST /api/alerts/mark_as_read/` - Mark alert as read

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/dashboard/chart_data/` - Get chart data

## Database Models

### Transaction
- `user` (ForeignKey): User who made the transaction
- `type` (CharField): 'income' or 'expense'
- `category` (CharField): Transaction category
- `amount` (DecimalField): Transaction amount
- `description` (CharField): Optional description
- `date` (DateField): Transaction date
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

### Budget
- `user` (ForeignKey): User who owns the budget
- `category` (CharField): Budget category
- `limit` (DecimalField): Monthly budget limit
- `month` (IntegerField): Month (1-12)
- `year` (IntegerField): Year
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

### BudgetAlert
- `user` (ForeignKey): User who receives the alert
- `budget` (ForeignKey): Related budget
- `alert_type` (CharField): 'warning' (75%) or 'critical' (90%)
- `spent_amount` (DecimalField): Amount spent
- `percentage` (DecimalField): Percentage of budget used
- `is_read` (BooleanField): Alert read status
- `created_at` (DateTimeField): Creation timestamp

## Features in Detail

### Smart Budgeting Suggestions
The application automatically monitors spending against set budgets and provides:
- **Warning Alerts**: When spending reaches 75% of budget limit
- **Critical Alerts**: When spending reaches 90% of budget limit
- **Category-based Tracking**: Separate budgets for different spending categories
- **Monthly Reset**: Budgets reset each month for fresh tracking

### Data Visualization
- **Expense Breakdown**: Doughnut chart showing expenses by category
- **Monthly Summary**: Income vs expenses comparison
- **Real-time Updates**: Dashboard updates automatically every 30 seconds

### User Experience
- **Modern Dark UI**: Professional dark theme with smooth animations
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Intuitive Navigation**: Clear menu structure and easy-to-use forms
- **Real-time Feedback**: Immediate confirmation of actions

## Testing

Run the test suite:
```bash
python manage.py test
```

## Security Features

- **Password Hashing**: Django's built-in password hashing with PBKDF2
- **CSRF Protection**: Cross-Site Request Forgery protection on all forms
- **Session Management**: Secure session handling
- **Input Validation**: Server-side validation of all inputs
- **Authentication Required**: Protected endpoints require user authentication

## Future Enhancements

- Integration with external financial APIs (banks, payment services)
- Recurring transaction support
- Mobile app version
- Advanced analytics and reporting
- Export functionality (PDF, CSV)
- Multi-currency support
- Notifications and reminders
- Machine learning-based spending predictions

## Deployment

### Production Deployment (Gunicorn + PostgreSQL)

1. Update `settings.py` for production:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Use PostgreSQL database
   - Set secure `SECRET_KEY`

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Run with Gunicorn:
```bash
gunicorn finance_tracker.wsgi:application --bind 0.0.0.0:8000
```

## License

This project is created for educational purposes as a diploma thesis at the University of Economics and Humanities, Sciences in Warsaw.

## Support

For issues or questions, please refer to the official documentation:
- Django: https://docs.djangoproject.com/
- Chart.js: https://www.chartjs.org/
- Bootstrap: https://getbootstrap.com/

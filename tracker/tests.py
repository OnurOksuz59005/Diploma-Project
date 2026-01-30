from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Transaction, Budget, BudgetAlert
from datetime import date
import json

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_transaction(self):
        response = self.client.post('/api/transactions/', {
            'type': 'expense',
            'category': 'food',
            'amount': 25.50,
            'date': '2024-01-15',
            'description': 'Lunch'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
    
    def test_get_transactions(self):
        Transaction.objects.create(
            user=self.user,
            type='expense',
            category='food',
            amount=25.50,
            date=date.today(),
            description='Lunch'
        )
        
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

class BudgetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_budget(self):
        response = self.client.post('/api/budgets/', {
            'category': 'food',
            'limit': 500.00,
            'month': 1,
            'year': 2024
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Budget.objects.count(), 1)
    
    def test_budget_alert_on_high_spending(self):
        budget = Budget.objects.create(
            user=self.user,
            category='food',
            limit=100.00,
            month=1,
            year=2024
        )
        
        Transaction.objects.create(
            user=self.user,
            type='expense',
            category='food',
            amount=95.00,
            date=date(2024, 1, 15)
        )
        
        self.assertEqual(BudgetAlert.objects.count(), 1)
        alert = BudgetAlert.objects.first()
        self.assertEqual(alert.alert_type, 'critical')

class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_stats(self):
        Transaction.objects.create(
            user=self.user,
            type='income',
            category='salary',
            amount=3000.00,
            date=date.today()
        )
        
        Transaction.objects.create(
            user=self.user,
            type='expense',
            category='food',
            amount=50.00,
            date=date.today()
        )
        
        response = self.client.get('/api/dashboard/stats/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(float(data['total_income']), 3000.00)
        self.assertEqual(float(data['total_expenses']), 50.00)
        self.assertEqual(float(data['balance']), 2950.00)

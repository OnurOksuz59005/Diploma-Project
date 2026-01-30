from django.db.models import Sum
from .models import Transaction, Budget, BudgetAlert
from datetime import datetime

def get_monthly_stats(user, month=None, year=None):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    transactions = Transaction.objects.filter(
        user=user,
        date__month=month,
        date__year=year
    )
    
    income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    
    return {
        'income': float(income),
        'expenses': float(expenses),
        'balance': float(income - expenses),
        'month': month,
        'year': year
    }

def get_category_breakdown(user, month=None, year=None):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    transactions = Transaction.objects.filter(
        user=user,
        type='expense',
        date__month=month,
        date__year=year
    )
    
    breakdown = {}
    for category_code, category_name in Transaction.CATEGORY_CHOICES:
        total = transactions.filter(category=category_code).aggregate(total=Sum('amount'))['total'] or 0
        if total > 0:
            breakdown[category_name] = float(total)
    
    return breakdown

def check_and_create_budget_alerts(user, month=None, year=None):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    budgets = Budget.objects.filter(user=user, month=month, year=year)
    
    for budget in budgets:
        spent = Transaction.objects.filter(
            user=user,
            type='expense',
            category=budget.category,
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        percentage = (spent / budget.limit * 100) if budget.limit > 0 else 0
        
        if percentage >= 90:
            BudgetAlert.objects.get_or_create(
                user=user,
                budget=budget,
                alert_type='critical',
                defaults={'spent_amount': spent, 'percentage': percentage}
            )
        elif percentage >= 75:
            BudgetAlert.objects.get_or_create(
                user=user,
                budget=budget,
                alert_type='warning',
                defaults={'spent_amount': spent, 'percentage': percentage}
            )

def get_spending_trends(user, months=6):
    from datetime import timedelta
    from django.utils import timezone
    
    trends = []
    now = timezone.now()
    
    for i in range(months):
        date = now - timedelta(days=30*i)
        month = date.month
        year = date.year
        
        stats = get_monthly_stats(user, month, year)
        stats['label'] = f"{month}/{year}"
        trends.append(stats)
    
    return list(reversed(trends))

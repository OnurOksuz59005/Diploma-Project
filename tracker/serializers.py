from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Transaction, Budget, BudgetAlert

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'category', 'amount', 'description', 'date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BudgetSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'limit', 'month', 'year', 'spent_amount', 'percentage_used', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_spent_amount(self, obj):
        from django.db.models import Sum
        spent = Transaction.objects.filter(
            user=obj.user,
            type='expense',
            category=obj.category,
            date__month=obj.month,
            date__year=obj.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        return float(spent)
    
    def get_percentage_used(self, obj):
        from django.db.models import Sum
        spent = Transaction.objects.filter(
            user=obj.user,
            type='expense',
            category=obj.category,
            date__month=obj.month,
            date__year=obj.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        if obj.limit > 0:
            return float((spent / obj.limit) * 100)
        return 0

class BudgetAlertSerializer(serializers.ModelSerializer):
    budget_category = serializers.CharField(source='budget.category', read_only=True)
    
    class Meta:
        model = BudgetAlert
        fields = ['id', 'budget_category', 'alert_type', 'spent_amount', 'percentage', 'is_read', 'created_at']
        read_only_fields = ['created_at']

class DashboardStatsSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    budget_alerts_count = serializers.IntegerField()
    transactions_count = serializers.IntegerField()

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Transaction, Budget, BudgetAlert
from .serializers import (
    TransactionSerializer, BudgetSerializer, BudgetAlertSerializer,
    DashboardStatsSerializer, UserSerializer
)
from django.contrib.auth.models import User

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self._check_budget_alerts(serializer.instance)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        self._check_budget_alerts(serializer.instance)
    
    def _check_budget_alerts(self, transaction):
        if transaction.type == 'expense':
            budget = Budget.objects.filter(
                user=transaction.user,
                category=transaction.category,
                month=transaction.date.month,
                year=transaction.date.year
            ).first()
            
            if budget:
                spent = Transaction.objects.filter(
                    user=transaction.user,
                    type='expense',
                    category=transaction.category,
                    date__month=transaction.date.month,
                    date__year=transaction.date.year
                ).aggregate(total=Sum('amount'))['total'] or 0
                
                percentage = (spent / budget.limit * 100) if budget.limit > 0 else 0
                
                if percentage >= 90:
                    BudgetAlert.objects.get_or_create(
                        user=transaction.user,
                        budget=budget,
                        alert_type='critical',
                        defaults={'spent_amount': spent, 'percentage': percentage}
                    )
                elif percentage >= 75:
                    BudgetAlert.objects.get_or_create(
                        user=transaction.user,
                        budget=budget,
                        alert_type='warning',
                        defaults={'spent_amount': spent, 'percentage': percentage}
                    )
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category')
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)
        
        queryset = self.get_queryset().filter(
            date__month=month,
            date__year=year
        )
        
        if category:
            queryset = queryset.filter(category=category)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)
        
        transactions = self.get_queryset().filter(
            date__month=month,
            date__year=year
        )
        
        income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'month': month,
            'year': year,
            'income': float(income),
            'expenses': float(expenses),
            'balance': float(income - expenses)
        })

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        now = timezone.now()
        budgets = self.get_queryset().filter(month=now.month, year=now.year)
        serializer = self.get_serializer(budgets, many=True)
        return Response(serializer.data)

class BudgetAlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BudgetAlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BudgetAlert.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        alerts = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        alert_id = request.data.get('alert_id')
        if alert_id:
            BudgetAlert.objects.filter(id=alert_id, user=request.user).update(is_read=True)
            return Response({'status': 'marked as read'})
        return Response({'error': 'alert_id required'}, status=status.HTTP_400_BAD_REQUEST)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        now = timezone.now()
        
        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=now.month,
            date__year=now.year
        )
        
        income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        
        alerts = BudgetAlert.objects.filter(user=request.user, is_read=False).count()
        
        data = {
            'total_income': float(income),
            'total_expenses': float(expenses),
            'balance': float(income - expenses),
            'budget_alerts_count': alerts,
            'transactions_count': transactions.count()
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)
        
        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        )
        
        expense_by_category = {}
        for category_code, category_name in Transaction.CATEGORY_CHOICES:
            total = transactions.filter(
                type='expense',
                category=category_code
            ).aggregate(total=Sum('amount'))['total'] or 0
            if total > 0:
                expense_by_category[category_name] = float(total)
        
        return Response({
            'expenses_by_category': expense_by_category,
            'month': month,
            'year': year
        })

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

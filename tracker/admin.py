from django.contrib import admin
from .models import Transaction, Budget, BudgetAlert

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'category', 'amount', 'date', 'created_at')
    list_filter = ('type', 'category', 'date', 'user')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', '-created_at')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'limit', 'month', 'year', 'created_at')
    list_filter = ('category', 'month', 'year', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BudgetAlert)
class BudgetAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'alert_type', 'percentage', 'is_read', 'created_at')
    list_filter = ('alert_type', 'is_read', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

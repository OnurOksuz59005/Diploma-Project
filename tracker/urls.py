from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet, BudgetViewSet, BudgetAlertViewSet,
    DashboardViewSet, UserViewSet
)
from .auth_views import register_view, login_view, logout_view, profile_view

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'alerts', BudgetAlertViewSet, basename='alert')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/register/', register_view, name='register'),
    path('auth/profile/', profile_view, name='profile'),
    path('auth/', include('rest_framework.urls')),
]

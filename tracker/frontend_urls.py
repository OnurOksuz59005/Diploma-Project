from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('transactions/', TemplateView.as_view(template_name='transactions.html'), name='transactions'),
    path('budgets/', TemplateView.as_view(template_name='budgets.html'), name='budgets'),
]

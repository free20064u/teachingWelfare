from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.financeDashboardView, name='finance_dashboard'),
]
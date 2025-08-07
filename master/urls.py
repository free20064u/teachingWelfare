from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.masterDashboardView, name='master_dashboard'),
]
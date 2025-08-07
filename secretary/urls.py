from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.secretaryDashboardView, name='secretary_dashboard'),
]
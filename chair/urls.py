from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.chairDashboardView, name='chair_dashboard'),
]
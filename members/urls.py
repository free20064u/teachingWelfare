from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('benefit/', views.benefitView, name='benefit'),
    path('benefitList/', views.benefitListView, name='benefitList'),
]
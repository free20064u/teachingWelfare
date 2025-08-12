from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.secretaryDashboardView, name='secretary_dashboard'),
    path('members/', views.membersListView, name='members_list'),
    path('members/<int:pk>/', views.memberDetailView, name='member_detail'),
    path('members/<int:pk>/edit/', views.memberEditView, name='member_edit'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.secretaryDashboardView, name='secretary_dashboard'),
    path('announcements/add/', views.announcement_add_view, name='add_announcement'),
    path('members/', views.membersListView, name='members_list'),
    path('members/<int:pk>/', views.memberDetailView, name='member_detail'),
    path('announcements/edit/<int:pk>/', views.announcement_edit_view, name='announcement_edit'),
    path('announcements/delete/<int:pk>/', views.announcement_delete_view, name='announcement_delete'),
    path('announcements/<int:pk>/dismiss/', views.dismiss_announcement_view, name='dismiss_announcement'),
    path('members/<int:pk>/edit/', views.memberEditView, name='member_edit'),
]
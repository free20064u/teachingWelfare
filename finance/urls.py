from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('dashboard/', views.financeDashboardView, name='finance_dashboard'),
    path('members/', views.financeMembersListView, name='finance_members_list'),
    path('member/<int:pk>/', views.financeMemberDetailView, name='finance_member_detail'),
    path('member/<int:pk>/print/', views.financeMemberStatementPrintView, name='finance_member_statement_print'),
    path('dues/<int:pk>/edit/', views.dues_edit_view, name='dues_edit'),
    path('dues/<int:pk>/delete/', views.dues_delete_view, name='dues_delete'),
]
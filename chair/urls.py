from django.urls import path
from . import views

app_name = 'chairperson'

urlpatterns = [
    path('dashboard/', views.chairDashboardView, name='chairperson_dashboard'),
    path('report/', views.financialReportView, name='financial_report'),
    path('benefits/', views.manageBenefitsView, name='manage_benefits'),
    path('benefit/<int:pk>/process/<str:action>/', views.processBenefitView, name='process_benefit'),
    path('member/<int:pk>/detail/', views.memberDetailView, name='member_detail'),
    path('announcement/<int:pk>/dismiss/', views.dismissAnnouncementView, name='dismiss_announcement'),
    path('member/<int:pk>/statement/print/', views.chairpersonMemberStatementPrintView, name='member_statement_print'),

]

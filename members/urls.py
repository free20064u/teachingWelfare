from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('benefit/', views.benefitView, name='benefit'),
    path('benefitList/', views.benefitListView, name='benefitList'),
    path('profile/', views.profileView, name='profile'),
    path('edit_profile/', views.editProfileView, name='edit_profile'),
]
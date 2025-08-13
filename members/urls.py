from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('benefit/', views.benefitView, name='benefit'),
    path('benefit-list/', views.benefitListView, name='benefit_list'),
    path('profile/', views.profileView, name='profile'),
    path('profile/edit/', views.editProfileView, name='edit_profile'),
    path('profile/spouse/', views.spouseView, name='spouse'),
    path('profile/children/', views.childrenView, name='children'),
    path('profile/parent/', views.parentView, name='parent'),
    path('profile/next-of-kin/', views.nextOfKinView, name='next_of_kin'),
    
    # New URL for the member's fund details/statement page
    path('fund-details/', views.fundDetailsView, name='fund_details'),
]
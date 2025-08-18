from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('benefit/', views.benefitView, name='benefit'),
    path('benefit-list/', views.benefitListView, name='benefit_list'),
    path('benefit/<int:pk>/edit/', views.benefit_editView, name='benefit_edit'),
    path('benefit/<int:pk>/delete/', views.benefit_deleteView, name='benefit_delete'),
    path('profile/', views.profileView, name='profile'),
    path('updates/', views.updatesView, name='updates'),
    path('profile/picture/', views.updateProfilePictureView, name='update_profile_picture'),
    path('profile/edit/', views.editProfileView, name='edit_profile'),
    path('profile/spouse/', views.spouseView, name='spouse'),
    path('profile/children/', views.childrenView, name='children'),
    path('profile/parent/', views.parentView, name='parent'),
    path('profile/next-of-kin/', views.nextOfKinView, name='next_of_kin'),
    
    # New URL for the member's fund details/statement page
    path('fund-details/', views.fundDetailsView, name='fund_details'),

    # URLs for password change
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='members/password_change_form.html',
             success_url=reverse_lazy('password_change_done')
         ),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='members/password_change_done.html'
         ),
         name='password_change_done'),
]
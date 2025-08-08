from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registerView, name='register'),
    path('editUser/', views.editUserView, name='edit_user')
]
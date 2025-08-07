from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.homepage, name='master_dashboard'),
]
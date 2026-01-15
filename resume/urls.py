from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('en/', views.en_home, name='home_en'),
]

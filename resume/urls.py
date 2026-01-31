from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('en/', views.en_home, name='home_en'),
    path('hu/', views.hu_home, name='home_hu'),
    path('contact/', views.contact, name='contact'),
    path('lab/', views.lab, name='lab'),
    
    # Theme-related URLs
    path('themes/', views.themes_gallery, name='themes'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('clear-theme/', views.clear_theme, name='clear_theme'),
]

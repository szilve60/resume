from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('en/', views.en_home, name='home_en'),
    path('hu/', views.hu_home, name='home_hu'),
    path('contact/', views.contact, name='contact'),
]

from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('booking/', views.booking, name='booking'),
    path('checkin/', views.checkin, name='checkin'),
    path('success/', views.success, name='success'),
    path('error/', views.error, name='error'),
]

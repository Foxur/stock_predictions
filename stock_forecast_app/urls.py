from django.urls import path
from stock_forecast_app import views

urlpatterns = [
    path('', views.home_site, name='home_site'),
]
from django.urls import path
from stock_forecast import views

urlpatterns = [
    path('', views.stock_forecast, name='stock_forecast'),
]
from django.urls import path
from stock_forecast import views

urlpatterns = [
    path('', views.subside_index, name='stock_forecast'),
    path("<int:pk>/", views.subside_detail, name="subside_detail"),
]
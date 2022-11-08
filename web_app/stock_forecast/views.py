
from django.shortcuts import render

def stock_forecast(request):
    return render(request, 'stock_forecast.html', {})
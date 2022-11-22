
from django.shortcuts import render
from stock_forecast.models import Subside
def subside_index(request):
    stock_forecast = Subside.objects.all()
    context = {
        'Projects': stock_forecast
    }
    return render(request, 'subside_index.html', context)

def subside_detail(request, pk):
    subside = Subside.objects.get(pk=pk)
    context = {
        'project': subside
    }
    return render(request, 'subside_detail.html', context)
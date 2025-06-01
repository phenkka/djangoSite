from django.shortcuts import render
from .models import GeneralStatistics, MainPageInfo

def home(request):
    info = MainPageInfo.objects.first()
    return render(request, 'main/home.html', {'info': info})

def statistics(request):
    stats = GeneralStatistics.objects.first()
    return render(request, 'main/statistics.html', {'stats': stats})

def demand(request):
    return render(request, 'main/demand.html')

def geo(request):
    return render(request, 'main/geo.html')

def skills(request):
    return render(request, 'main/skills.html')

def latest_vacancies(request):
    return render(request, 'main/latest.html')

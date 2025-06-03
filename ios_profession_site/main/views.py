from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import GeneralStatistics, MainPageInfo, DemandStatistics, GeoStatistics, SkillsStatistics
from .forms import EmailLoginForm, RegisterForm


def home(request):
    info = MainPageInfo.objects.first()
    return render(request, 'main/home.html', {'info': info})

def statistics(request):
    stats = GeneralStatistics.objects.first()
    return render(request, 'main/statistics.html', {'stats': stats})

def demand(request):
    stats = DemandStatistics.objects.first()
    return render(request, 'main/demand.html', {'stats': stats})

def geo(request):
    stats = GeoStatistics.objects.first()
    return render(request, 'main/geo.html', {'stats': stats})

def skills(request):
    stats = SkillsStatistics.objects.first()
    return render(request, 'main/skills.html', {'stats': stats})

def latest_vacancies(request):
    return render(request, 'main/latest.html')

def register(request):
    return render(request, 'main/register.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login(request):
    return render(request, 'main/login.html')

def custom_login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
    else:
        form = EmailLoginForm()
    return render(request, 'main/login.html', {'form': form})
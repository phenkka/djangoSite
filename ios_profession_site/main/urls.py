from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('demand/', views.demand, name='demand'),
    path('geo/', views.geo, name='geo'),
    path('skills/', views.skills, name='skills'),
    path('latest/', views.latest_vacancies, name='latest_vacancies'),
]

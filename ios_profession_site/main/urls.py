from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import custom_login_view, activate

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('demand/', views.demand, name='demand'),
    path('geo/', views.geo, name='geo'),
    path('skills/', views.skills, name='skills'),
    path('latest/', views.latest_vacancies, name='latest_vacancies'),
    path('login/', custom_login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('download-csv/<str:filename>/', views.download_csv, name='download_csv'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
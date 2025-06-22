import os
import csv

from pandas.core.indexes.base import str_t

from .models import GeneralStatistics, MainPageInfo, DemandStatistics, GeoStatistics, SkillsStatistics, HHStatistics
from .forms import EmailLoginForm, RegisterForm

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import HttpResponse, FileResponse, Http404


@login_required
def download_csv(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'csv', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Файл не найден")

def read_csv(file_field):
    if file_field and file_field.path:
        with open(file_field.path, encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return ''

            max_rows = 10  # Максимум строк с данными (без заголовка)

            html = '<table class="data-table">\n'
            # Заголовок
            html += '<thead><tr>' + ''.join(f'<th>{escape(col)}</th>' for col in rows[0]) + '</tr></thead>\n'
            html += '<tbody>\n'

            # Отображаем либо все строки, если их меньше max_rows, либо первые max_rows
            data_rows = rows[1:]
            if len(data_rows) > max_rows:
                for row in data_rows[:max_rows]:
                    html += '<tr>' + ''.join(f'<td>{escape(cell)}</td>' for cell in row) + '</tr>\n'
                # Добавляем строку с многоточиями, по количеству колонок
                html += '<tr>' + ''.join('<td>...</td>' for _ in rows[0]) + '</tr>\n'
            else:
                for row in data_rows:
                    html += '<tr>' + ''.join(f'<td>{escape(cell)}</td>' for cell in row) + '</tr>\n'

            html += '</tbody></table>'

            return mark_safe(html)
    return ''


def home(request):
    info = MainPageInfo.objects.first()
    return render(request, 'main/home.html', {'info': info})

def statistics(request):
    stats = GeneralStatistics.objects.first()

    salary_dynamics_table = read_csv(stats.salary_dynamics_csv)
    vacancies_dynamics_table = read_csv(stats.vacancies_dynamics_csv)
    salary_by_city_table = read_csv(stats.salary_by_city_csv)
    vacancies_share_by_city_table = read_csv(stats.vacancies_share_by_city_csv)
    top_skills_table = read_csv(stats.top_skills_csv)

    context = {
        'stats': stats,
        'tables': [
            {
                'title': 'Динамика уровня зарплат по годам',
                'html': salary_dynamics_table,
            },
            {
                'title': 'Динамика количества вакансий по годам',
                'html': vacancies_dynamics_table,
            },
            {
                'title': 'Уровень зарплат по городам',
                'html': salary_by_city_table,
            },
            {
                'title': 'Доля вакансий по городам',
                'html': vacancies_share_by_city_table,
            },
            {
                'title': 'ТОП-20 навыков по годам',
                'html': top_skills_table,
            },
        ]
    }

    return render(request, 'main/statistics.html', context)

def demand(request):
    stats = DemandStatistics.objects.first()

    ios_salary_level_trend_table = read_csv(stats.ios_salary_level_trend_csv)
    ios_vacancies_level_trend_table = read_csv(stats.ios_vacancies_level_trend_csv)

    context = {
        'stats': stats,
        'tables': [
            {
                'title': 'Динамика уровня зарплат по годам для выбранной профессии',
                'html': ios_salary_level_trend_table,
            },
            {
                'title': 'Динамика количества вакансий по годам для выбранной профессии',
                'html': ios_vacancies_level_trend_table,
            },
        ]
    }

    return render(request, 'main/demand.html', context)

def geo(request):
    stats = GeoStatistics.objects.first()

    geo_ios_city_salary_table = read_csv(stats.geo_ios_city_salary_csv)
    geo_ios_city_vacancy_share_table = read_csv(stats.geo_ios_city_vacancy_share_csv)

    context = {
        'stats': stats,
        'tables': [
            {
                'title': 'Уровень зарплат по городам для выбранной профессии',
                'html': geo_ios_city_salary_table,
            },
            {
                'title': 'Доля вакансий по городам для выбранной профессии',
                'html': geo_ios_city_vacancy_share_table,
            },
        ]
    }

    return render(request, 'main/geo.html', context)

def skills(request):
    stats = SkillsStatistics.objects.first()

    skills_top_ios_trend_table = read_csv(stats.skills_top_ios_trend_csv)

    context = {
        'stats': stats,
        'tables': [
            {
                'title': 'ТОП-20 навыков по годам для выбранной профессии',
                'html': skills_top_ios_trend_table,
            },
        ]
    }

    return render(request, 'main/skills.html', context)

def latest_vacancies(request):
    vacancies = HHStatistics.objects.order_by('-published_at')[:20]
    return render(request, 'main/latest_vacancies.html', {'vacancies': vacancies})

def register(request):
    email_sent = False
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            email_sent = True
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form, 'email_sent': email_sent})

def custom_login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
    else:
        form = EmailLoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Подтверждение регистрации'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"
    message = render_to_string('main/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })
    send_mail(mail_subject, message, 'from@example.com', [user.email])

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Активная ссылка недействительна!')
import os

from .models import GeneralStatistics, MainPageInfo, DemandStatistics, GeoStatistics, SkillsStatistics
from .forms import EmailLoginForm, RegisterForm

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
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
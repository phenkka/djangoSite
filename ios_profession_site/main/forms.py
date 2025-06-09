from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Почта', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))
    captcha = CaptchaField()

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Неверный email или пароль")

        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError("Неверный email или пароль")

        self.user = user
        return self.cleaned_data

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Подтверждение пароля'}), label="Повторите пароль")
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'captcha']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Почта'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data
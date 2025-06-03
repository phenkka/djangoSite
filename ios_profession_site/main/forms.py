from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

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
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'captcha']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data
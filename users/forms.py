from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from team_finder.constants import USER_NAME_MAX_LENGTH, USER_SURNAME_MAX_LENGTH
from users.models import User
from users.validators import validate_github_url, validate_phone_format


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=USER_NAME_MAX_LENGTH, label="Имя")
    surname = forms.CharField(max_length=USER_SURNAME_MAX_LENGTH, label="Фамилия")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
        )


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(
                self.request,
                username=email.lower(),
                password=password,
            )
            if self.user is None:
                raise forms.ValidationError(
                    "Неверный email или пароль",
                    code="invalid_login",
                )
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")

    def clean_phone(self):
        phone = validate_phone_format(self.cleaned_data["phone"])
        qs = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Этот номер телефона уже используется.")
        return phone

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Текущий пароль"
        self.fields["new_password1"].label = "Новый пароль"
        self.fields["new_password2"].label = "Подтвердите новый пароль"

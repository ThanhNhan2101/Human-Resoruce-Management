from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Sai tài khoản hoặc mật khẩu")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

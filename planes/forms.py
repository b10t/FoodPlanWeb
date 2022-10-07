from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)

    password = None

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введённые пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    class Meta:
        model = get_user_model()

        fields = ('username', 'email')

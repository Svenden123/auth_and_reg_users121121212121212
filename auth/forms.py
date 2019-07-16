from django import forms
from django.contrib.auth.models import User
from django.forms import Form, PasswordInput



class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=30, error_messages={'required': 'Укажите логин'})
    password = forms.CharField(label='Пароль', widget=PasswordInput, error_messages={'required': 'Укажите пароль'})

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=30, error_messages={'required': 'Укажите логин'})
    password = forms.CharField(label='Пароль', widget=PasswordInput, error_messages={'required': 'Укажите пароль'})
    password2 = forms.CharField(label='Пароль (еще раз)', widget=PasswordInput,
        error_messages={'required': 'Укажите пароль еще раз'})

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли должны совпадать!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

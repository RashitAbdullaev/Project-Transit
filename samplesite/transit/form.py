from django.forms import ModelForm,DateTimeInput
from allauth.account.forms import SignupForm
import calendar
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Request


# Форма регистрации пользователя
class MyCustomUserCreatingForm(UserCreationForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    initial='Роль')

    class Meta:
        model = User
        fields = ('username', 'email', 'groups',)


class MyCustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups',)


# Форма добавления заявок
class RequestForm(ModelForm):
    time = forms.CharField(
        widget=forms.TextInput(attrs={'class':'date','type':'date'})
    )

    class Meta:
        model = Request
        fields = ('name', 'direction', 'type', 'time', 'weight', 'measure_name')

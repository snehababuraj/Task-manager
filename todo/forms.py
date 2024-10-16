from django import forms
from todo.models import Todo
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=("id","created_date","status","user_object")
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control mb-3"}),
            # "user":forms.TextInput(attrs={"class":"form-control mb-3"})
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

class LoginForm(forms.Form):

    username=forms.CharField(max_length=200)

    password=forms.CharField(max_length=200)
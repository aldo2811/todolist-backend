from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Todolist


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class TaskForm(forms.Form):
    title = forms.CharField(label="Title: ", max_length=100, required=True)
    description = forms.CharField(label="Description: ", max_length=500, required=True)
    category = forms.ModelChoiceField(
        label="Category: ", queryset=Category.objects.filter()
    )
    date_due = forms.DateField(
        label="Date Due: ",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "datetimepicker"}),
        required=True,
    )


class CategoryForm(forms.Form):
    name = forms.CharField(label="Category: ", max_length=100, required=True)
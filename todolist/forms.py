from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Category


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
    STATUS = (
        (1, _('High')),
        (2, _('Mid')),
        (3, _('Low'))
    )

    title = forms.CharField(label="Title: ", max_length=100, required=True)
    description = forms.CharField(label="Description: ", max_length=500, required=True)
    category = forms.ModelChoiceField(
        label="Category: ", queryset=Category.objects.filter()
    )
    priority = forms.ChoiceField(
        label="Priority: ", choices=STATUS
    )
    date_due = forms.DateField(
        label="Date Due: ",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "datetimepicker"}),
        required=True,
    )


class CategoryForm(forms.Form):
    name = forms.CharField(label="Category: ", max_length=100, required=True)

from django import forms
from .models import Category, Todolist


class TaskForm(forms.Form):
    title = forms.CharField(label="Title: ", max_length=100, required=True)
    description = forms.CharField(label="Description: ", max_length=500, required=True)
    category = forms.ModelChoiceField(
        label="Category: ", queryset=Category.objects.all(), required=True
    )
    todolist = forms.ModelChoiceField(
        label="Todolist: ", queryset=Todolist.objects.all(), required=True
    )
    datetime_due = forms.DateField(
        label="Date Due: ",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        widget=forms.DateInput(attrs={"class": "datetimepicker"}),
        required=True,
    )

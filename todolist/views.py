from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.views import View

from .forms import TaskForm, CreateUserForm
from .models import Task, Category, Todolist, User


# Create your views here.
class TaskList(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, "task_list.html", {"task_list": tasks})


class TaskDetail(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        return render(request, "task_detail.html", {"task": task})


class TaskCreate(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "task_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        category = request.POST["category"]
        todolist = request.POST["todolist"]
        title = request.POST["title"]
        description = request.POST["description"]
        datetime_due = request.POST["datetime_due"]

        Task.objects.create(
            category=Category.objects.get(pk=category),
            todolist=Todolist.objects.get(pk=todolist),
            title=title,
            description=description,
            datetime_due=datetime_due,
        )

        form = TaskForm()
        return render(request, "task_create.html", {"form": form})


class UserCreate(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, "user_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
        else:
            return render(
                request, "user_create.html", {"form": form, "error": form.errors}
            )


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, "user_login.html", {"form": form, "error": ""})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]

        form = AuthenticationForm()

        try:
            User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                raise ValidationError("Incorrect password. Please try again.")
        except ObjectDoesNotExist:
            error = "Username does not exist. Please try again."
            return render(request, "user_login.html", {"form": form, "error": error})
        except ValidationError as e:
            return render(
                request, "user_login.html", {"form": form, "error": e.message}
            )

        return redirect("task_list")

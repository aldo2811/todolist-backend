from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.shortcuts import render, redirect
from django.views import View

from .forms import TaskForm, CreateUserForm
from .models import Task, Category, Todolist, User


# Create your views here.
class TaskList(View):
    def get(self, request, *args, **kwargs):
        try:
            todolist = Todolist.objects.get(user=request.user)
            tasks = Task.objects.filter(todolist=todolist)
        except ObjectDoesNotExist:
            tasks = Todolist.objects.none()
        return render(request, "task_list.html", {"task_list": tasks})


class TaskDetail(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        todolist = task.todolist
        if todolist.user != request.user:
            raise PermissionDenied
        return render(request, "task_detail.html", {"task": task})


class TaskCreate(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "task_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        category = request.POST["category"]
        title = request.POST["title"]
        description = request.POST["description"]
        datetime_due = request.POST["datetime_due"]

        todolist = Todolist.objects.get(user=request.user)

        Task.objects.create(
            category=Category.objects.get(pk=category),
            todolist=todolist,
            title=title,
            description=description,
            datetime_due=datetime_due,
        )

        return redirect("task_list")


class UserCreate(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, "user_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            Todolist.objects.create(user=request.user)
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

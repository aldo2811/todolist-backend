from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.shortcuts import render, redirect
from django.views import View

from datetime import date, datetime, time

from .forms import TaskForm, CreateUserForm
from .models import Task, Category, Todolist, User


# Create your views here.
class TaskList(View):
    def get(self, request, *args, **kwargs):
        try:
            cur_datetime = datetime.today()
            today_max = datetime.combine(date.today(), time.max)

            todolist = Todolist.objects.get(user=request.user)
            tasks = Task.objects.filter(todolist=todolist)

            today_tasks = tasks.filter(datetime_due__range=[cur_datetime, today_max])
            overdue_tasks = tasks.filter(datetime_due__lt=cur_datetime)
            upcoming_tasks = tasks.filter(datetime_due__gt=cur_datetime)

        except ObjectDoesNotExist:
            overdue_tasks = Todolist.objects.none()
            today_tasks = Todolist.objects.none()
            upcoming_tasks = Todolist.objects.none()
        return render(
            request,
            "task_list.html",
            {
                "overdue_tasks": overdue_tasks,
                "today_tasks": today_tasks,
                "upcoming_tasks": upcoming_tasks,
            },
        )


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


class TaskUpdate(View):
    def dispatch(self, request, *args, **kwargs):
        method = request.POST.get("_method", "").lower()
        if method == "put":
            return self.put(request, *args, **kwargs)
        return super(TaskUpdate, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        todolist = task.todolist
        if todolist.user != request.user:
            raise PermissionDenied

        form = TaskForm(
            initial={
                "title": task.title,
                "description": task.description,
                "category": task.category,
                "datetime_due": task.datetime_due,
            }
        )

        return render(
            request,
            "task_update.html",
            {"form": form, "task_id": self.kwargs["task_id"]},
        )

    def put(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data
            task_obj = Task.objects.get(pk=self.kwargs["task_id"])
            todolist = task_obj.todolist
            if todolist.user != request.user:
                raise PermissionDenied

            task_obj.title = task["title"]
            task_obj.description = task["description"]
            task_obj.category = task["category"]
            task_obj.datetime_due = task["datetime_due"]

            task_obj.save()

        return redirect("task_list")


class TaskDelete(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        todolist = task.todolist
        if todolist.user != request.user:
            raise PermissionDenied

        task.delete()
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

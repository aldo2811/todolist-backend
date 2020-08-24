from django.shortcuts import render
from django.views import View
from .models import Task, Category, Todolist
from .forms import TaskForm


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

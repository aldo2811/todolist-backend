from django.shortcuts import render
from django.views import View
from todolist.models import Task


# Create your views here.
class TaskView(View):
  def get(self, request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'task_list': tasks})


class TaskDetailView(View):
  def get(self, request, **kwargs):
    task = Task.objects.get(pk=self.kwargs['task_id'])
    return render(request, 'task_detail.html', {'task': task})

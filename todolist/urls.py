from django.urls import path

from todolist import views

urlpatterns = [
  path('task/', views.TaskView.as_view(), name='task_list'),
  path('task/<int:task_id>', views.TaskDetailView.as_view(), name='task_detail')
]
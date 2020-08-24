from django.urls import path

from todolist import views

urlpatterns = [
    path("task/", views.TaskList.as_view(), name="task_list"),
    path("task/<int:task_id>", views.TaskDetail.as_view(), name="task_detail"),
    path("task/new", views.TaskCreate.as_view(), name="task_create"),
]

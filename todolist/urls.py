from django.urls import path

from todolist import views

urlpatterns = [
    path("register/", views.UserCreate.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("task/", views.TaskList.as_view(), name="task_list"),
    path("task/new", views.TaskCreate.as_view(), name="task_create"),
    path("task/<int:task_id>", views.TaskDetail.as_view(), name="task_detail"),
    path("task/<int:task_id>/update", views.TaskUpdate.as_view(), name="task_update"),
    path("task/<int:task_id>/delete", views.TaskDelete.as_view(), name="task_delete"),
]

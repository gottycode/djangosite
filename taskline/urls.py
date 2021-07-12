from django.urls import path

from taskline.views import TaskListView
from taskline.views import CreateTaskView
from taskline.views import UpdateTaskView
from taskline.views import DeleteTaskView


urlpatterns = [
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('create_task/', CreateTaskView.as_view(), name='create_task'),
    path('update_task/', UpdateTaskView.as_view(), name='update_task'),
    path('delete_task/', DeleteTaskView.as_view(), name='delete_task'),
]

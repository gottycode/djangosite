from django.urls import path

from taskline.views import TaskListView
from taskline.views import TaskListSearchView
from taskline.views import lazy_load_tasks
from taskline.views import CreateTaskView
from taskline.views import UpdateTaskView
from taskline.views import DeleteTaskView

app_name = 'taskline'


urlpatterns = [
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('task_list_search/', TaskListSearchView.as_view(), name='task_list_search'),
    path('lazy_load_tasks/', lazy_load_tasks, name='lazy_load_tasks'),
    path('create_task/', CreateTaskView.as_view(), name='create_task'),
    path('update_task/<int:id>', UpdateTaskView.as_view(), name='update_task'),
    path('delete_task/<int:id>', DeleteTaskView.as_view(), name='delete_task'),
]

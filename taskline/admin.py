from django.contrib import admin

from taskline.models import Task
from taskline.models import TaskCategory

admin.site.register(Task)
admin.site.register(TaskCategory)

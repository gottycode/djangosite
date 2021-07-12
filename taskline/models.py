from django.db import models

from appauth.models import AppUser


class TaskCategory(models.Model):
    task_category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.task_category_name


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    task_resource = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    work_hours = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.task_name

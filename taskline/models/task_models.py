from django.db import models

from appauth.models import AppUser


class TaskCategory(models.Model):
    task_category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.task_category_name


class Task(models.Model):
    # 名前
    task_name = models.CharField(max_length=200)
    task_category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    task_resource = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    work_hours = models.DecimalField(max_digits=5, decimal_places=2)  # 小数以下2桁、全体5桁
    progress_rate = models.FloatField('進捗率', blank=True, null=True)
    duration = models.DecimalField('期間', max_digits=5, decimal_places=2, blank=True, null=True)
    planed_hours = models.DecimalField('予定工数', max_digits=5, decimal_places=2, blank=True, null=True)
    actual_hours = models.DecimalField('実績工数', max_digits=5, decimal_places=2, blank=True, null=True)
    planned_start_datetime = models.DateTimeField('予定開始日時', blank=True, null=True)
    planned_end_datetime = models.DateTimeField('予定終了日時', blank=True, null=True)
    actual_start_datetime = models.DateTimeField('実績開始日時', blank=True, null=True)
    actual_end_datetime = models.DateTimeField('実績終了日時', blank=True, null=True)
    memo = models.TextField('備考', max_length=50, blank=True)
    is_milestone = models.BooleanField('マイルストーン', default=False)
    picture = models.FileField(upload_to='student/', blank=True)

    def __str__(self):
        return self.task_name

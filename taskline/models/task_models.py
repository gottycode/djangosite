from django.db.models import Model
from django.db.models import (CharField, DecimalField,
                              FloatField, DateTimeField,
                              TextField, BooleanField, FileField)
from django.db.models import ForeignKey, CASCADE
from accounts.models import AppUser


# class BaseModel(Model):
#     created_at = DateTimeField(auto_now=True)
#     updated_at = DateTimeField(auto_now_add=True)


class TaskCategory(Model):
    task_category_name = CharField(max_length=100)

    def __str__(self):
        return self.task_category_name


class Task(Model):
    # 名前
    task_name = CharField(max_length=200)
    task_category = ForeignKey(TaskCategory, on_delete=CASCADE)
    task_resource = ForeignKey(AppUser, on_delete=CASCADE)
    work_hours = DecimalField(max_digits=5, decimal_places=2)  # 小数以下2桁、全体5桁
    progress_rate = FloatField('進捗率', blank=True, null=True)
    duration = DecimalField('期間', max_digits=5, decimal_places=2, blank=True, null=True)
    planed_hours = DecimalField('予定工数', max_digits=5, decimal_places=2, blank=True, null=True)
    actual_hours = DecimalField('実績工数', max_digits=5, decimal_places=2, blank=True, null=True)
    planned_start_datetime = DateTimeField('予定開始日時', blank=True, null=True)
    planned_end_datetime = DateTimeField('予定終了日時', blank=True, null=True)
    actual_start_datetime = DateTimeField('実績開始日時', blank=True, null=True)
    actual_end_datetime = DateTimeField('実績終了日時', blank=True, null=True)
    memo = TextField('備考', max_length=50, blank=True)
    is_milestone = BooleanField('マイルストーン', default=False)
    picture = FileField(upload_to='student/', blank=True)

    def __str__(self):
        return self.task_name

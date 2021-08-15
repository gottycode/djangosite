import datetime

from accounts.models import AppUser
from django.forms import (DecimalField, CharField, FloatField,
                          ModelChoiceField, TextInput, ValidationError,
                          DateTimeField, DateTimeInput, DurationField)
from django.forms import ModelForm, Form

from taskline.models import Task
from taskline.models import TaskCategory


class CreateTaskForm(ModelForm):

    # TODO  {{ form.as_p }}以外効かない？
    # error_css_class = 'is-invalid'

    task_name = CharField(
        max_length=5,
        initial='',
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '名前'
            }
        )
    )
    work_hours = DecimalField(
        initial=0.0,
        max_value=160,
        min_value=0,
        decimal_places=2,
        widget=TextInput(
            attrs={
                'class': 'form-control'
            }
        ))
    task_resource = ModelChoiceField(queryset=AppUser.objects.all())
    task_category = ModelChoiceField(queryset=TaskCategory.objects.all())

    progress_rate = FloatField(required=False, min_value=0, max_value=100)
    duration = DurationField(required=False)
    planed_hours = DecimalField(required=False)
    actual_hours = DecimalField(required=False)
    planned_start_datetime = DateTimeField(
        required=False,
        widget=DateTimeInput(
            attrs={"type": "datetime-local",
                   "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    planned_end_datetime = DateTimeField(required=False,
                                         widget=DateTimeInput(
                                             attrs={"type": "datetime-local",
                                                    "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    actual_start_datetime = DateTimeField(required=False,
                                          widget=DateTimeInput(
                                              attrs={"type": "datetime-local",
                                                     "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    actual_end_datetime = DateTimeField(required=False,
                                        widget=DateTimeInput(
                                            attrs={"type": "datetime-local",
                                                   "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    # picture = FileField(label='ファイルアップロード')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_resource'].widget.attrs["class"] = "form-control"
        self.fields['task_category'].widget.attrs["class"] = "form-control"

    def clean(self):
        # TODO 項目間の相関チェックやＤＢなどの状態チェック
        return super().clean()

    def clean_planned_end_datetime(self):

        # 開始≦終了のチェック
        planned_start_datetime = self.cleaned_data['planned_start_datetime']
        planned_end_datetime = self.cleaned_data['planned_end_datetime']
        if planned_start_datetime and planned_end_datetime:
            if planned_start_datetime > planned_end_datetime:
                raise ValidationError("開始≦終了にしてください")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return planned_end_datetime

    class Meta:
        model = Task
        fields = ['task_name', 'task_resource', 'work_hours', 'task_category']


class UpdateTaskForm(CreateTaskForm):
    # とりあえずCreateを使う
    pass


class SearchTaskForm(Form):
    task_name = CharField(initial='', max_length=5, required=False)
    work_hours = DecimalField(required=False)


class DeleteTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = []

import datetime

from appauth.models import AppUser
from django import forms
from django.core.exceptions import ValidationError

from taskline.models import Task
from taskline.models import TaskCategory


class CreateTaskForm(forms.ModelForm):

    # TODO  {{ form.as_p }}以外効かない？
    # error_css_class = 'is-invalid'

    task_name = forms.CharField(
        max_length=5,
        initial='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '名前'
            }
        )
    )
    work_hours = forms.DecimalField(
        initial=0.0,
        max_value=160,
        min_value=0,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ))
    task_resource = forms.ModelChoiceField(queryset=AppUser.objects.all())
    task_category = forms.ModelChoiceField(queryset=TaskCategory.objects.all())

    progress_rate = forms.FloatField(required=False, min_value=0, max_value=100)
    duration = forms.DurationField(required=False)
    planed_hours = forms.DecimalField(required=False)
    actual_hours = forms.DecimalField(required=False)
    planned_start_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local",
                   "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    planned_end_datetime = forms.DateTimeField(required=False,
                                               widget=forms.DateTimeInput(
                                                   attrs={"type": "datetime-local",
                                                          "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    actual_start_datetime = forms.DateTimeField(required=False,
                                                widget=forms.DateTimeInput(
                                                    attrs={"type": "datetime-local",
                                                           "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    actual_end_datetime = forms.DateTimeField(required=False,
                                              widget=forms.DateTimeInput(
                                                  attrs={"type": "datetime-local",
                                                         "value": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}))
    # picture = forms.FileField(label='ファイルアップロード')

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


class SearchTaskForm(forms.Form):
    task_name = forms.CharField(initial='', max_length=5,)
    work_hours = forms.DecimalField()


class DeleteTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

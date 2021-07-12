from django import forms

from taskline.models import Task


class CreateTaskForm(forms.Form):
    task_name = forms.CharField(max_length=5)
    work_hours = forms.DecimalField(max_value=200)

    class Meta:
        model = Task
        fields = '__all__'


class UpdateTaskForm(forms.Form):
    task_name = forms.CharField(max_length=5)
    work_hours = forms.DecimalField(max_value=200)

    class Meta:
        model = Task
        fields = '__all__'


class DeleteTaskForm(forms.Form):
    class Meta:
        model = Task
        fields = []

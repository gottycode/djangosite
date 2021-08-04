import os
from typing import ContextManager
from django.contrib import messages
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.db.models import Q

from taskline.models import Task
from taskline.forms import CreateTaskForm
from taskline.forms import UpdateTaskForm
from taskline.forms import DeleteTaskForm
from taskline.forms import SearchTaskForm


class TaskListView(View):
    """タスク一覧"""

    def get(self, request, *args, **kwargs):

        tasks = Task.objects.all()[:5]

        context = {
            'tasks': tasks
        }
        return render(request, 'taskline/task_list.html', context)


class TaskListSearchView(View):

    def get(self, request, *args, **kwargs):
        form = SearchTaskForm(request.GET or None)

        # print(form.is_valid)
        # print(form.errors)
        if form.is_valid():

            task_name = request.GET.get('task_name')
            work_hours = request.GET.get('work_hours')
            form = SearchTaskForm
            tasks = Task.objects.filter(Q(task_name=task_name) | Q(work_hours=work_hours))
            context = {
                'tasks': tasks,
                'form': form
            }
            return render(request, 'taskline/task_list_search.html', context)
        else:
            message = 'エラーがあります。再入力してください'
            context = {
                'form': form,
                'message': message
            }
            return render(request, 'taskline/task_list_search.html', context)


def lazy_load_tasks(request):
    page = request.POST.get('page')
    tasks = Task.objects.all()

    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = 5
    paginator = Paginator(tasks, results_per_page)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(2)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    # build a html posts list with the paginated tasks
    tasks_html = loader.render_to_string('taskline/tasks.html', {'tasks': tasks})

    # package output data and return it as a JSON object
    output_data = {'tasks_html': tasks_html, 'has_next': tasks.has_next()}
    return JsonResponse(output_data)


class CreateTaskView(View):
    template_name = os.path.join('taskline', 'create_task.html')

    def get(self, request, *args, **kwargs):
        form = CreateTaskForm
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST or None)

        # print(form.is_valid)
        # print(form.errors)
        if form.is_valid():
            form.save()
            # TODO Taskに登録者を含める
            # task = form.save(commit=False)
            # task.登録者 = request.user
            # task.save()

            messages.success(request, "登録成功しました")
            return redirect('taskline:task_list')

        else:
            message = 'エラーがあります。再入力してください'
            context = {
                'form': form,
                'message': message
            }
            return render(request, self.template_name, context)


class UpdateTaskView(View):
    template_name = os.path.join('taskline', 'create_task.html')

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        task = get_object_or_404(Task, pk=id)
        form = UpdateTaskForm(request.POST or None, instance=task)
        context = {
            'form': form,
        }
        return render(request, 'taskline/create_task.html', context)

    def post(self, request, *args, **kwargs):

        id = kwargs['id']
        task = get_object_or_404(Task, pk=id)
        form = UpdateTaskForm(request.POST or None, instance=task)
        if form.is_valid:
            form.save()
            return redirect('taskline:task_list')

        else:
            message = '再入力してください'
            context = {
                'form': form,
                'message': message
            }
            return render(request, self.template_name, context)


class DeleteTaskView(View):
    template_name = os.path.join('taskline', 'delete_task.html')

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        task = get_object_or_404(Task, pk=id)
        form = DeleteTaskForm(request.POST or None, instance=task)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        id = kwargs['id']
        task = get_object_or_404(Task, pk=id)
        form = UpdateTaskForm(request.POST or None, instance=task)
        if form.is_valid:
            task.delete()
            return redirect('taskline:task_list')

        else:
            message = '再入力してください'
            context = {
                'form': form,
                'message': message
            }
            return render(request, self.template_name, context)

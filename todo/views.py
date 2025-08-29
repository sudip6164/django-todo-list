from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Task, Category
from datetime import datetime

def index(request):
    tasks_qs = Task.objects.all().order_by('completed', 'due_date')
    paginator = Paginator(tasks_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'todo/index.html', {'page_obj': page_obj})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'M')
        category_name = request.POST.get('category', '').strip()
        due_date_str = request.POST.get('due_date', None)

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M")

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date,
                priority=priority,
                description=description,
                category=category,
            )
        return redirect('index')

    return render(request, 'todo/add.html')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'M')
        category_name = request.POST.get('category', '').strip()
        due_date_str = request.POST.get('due_date', None)

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M")

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        task.title = title or task.title
        task.description = description
        task.priority = priority
        task.category = category
        task.due_date = due_date
        task.save()
        return redirect('index')

    return render(request, 'todo/edit.html', {'task': task})

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('index')

def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

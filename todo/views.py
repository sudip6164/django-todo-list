from django.shortcuts import render, redirect
from .models import Task, Category
from datetime import datetime

def index(request):
    tasks = Task.objects.all().order_by('completed', 'due_date')
    return render(request, 'todo/index.html', {'tasks': tasks})

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

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('index')

def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

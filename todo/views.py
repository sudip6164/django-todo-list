from django.shortcuts import render, redirect
from .models import Task

def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date') or None
        priority = request.POST.get('priority') or 'M'
        if title:
            Task.objects.create(title=title, due_date=due_date, priority=priority)
        return redirect('index')

    tasks = Task.objects.all().order_by('completed', 'due_date')
    return render(request, 'todo/index.html', {'tasks': tasks})

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('index')

def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

from django.shortcuts import render, redirect
from .models import Task, Category

def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date', None)
        priority = request.POST.get('priority', 'M')
        category_name = request.POST.get('category', '').strip()

        category = None
        if category_name:  
            category, _ = Category.objects.get_or_create(name=category_name)

        if title:
            Task.objects.create(title=title, due_date=due_date, priority=priority, category=category)
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

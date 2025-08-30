from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Task, Category
from django.db.models import Q
from datetime import datetime
from django.utils import timezone

def index(request):
    # Get all tasks and apply smart ordering
    tasks_qs = Task.objects.all()
    
    # Apply smart ordering: overdue first, then due today, then by due date
    tasks_qs = sorted(tasks_qs, key=lambda x: (x.get_ordering_value(), x.due_date or timezone.now() + timezone.timedelta(days=365)))
    
    # Basic search
    query = request.GET.get('q', '').strip()
    if query:
        tasks_qs = [task for task in tasks_qs if query.lower() in task.title.lower() or query.lower() in task.description.lower()]
    
    # Basic filters
    priority = request.GET.get('priority', '')
    if priority in ['L', 'M', 'H']:
        tasks_qs = [task for task in tasks_qs if task.priority == priority]
    
    category_name = request.GET.get('category', '').strip()
    if category_name:
        tasks_qs = [task for task in tasks_qs if task.category and task.category.name.lower() == category_name.lower()]
    
    completed = request.GET.get('completed', '')
    if completed == 'true':
        tasks_qs = [task for task in tasks_qs if task.completed]
    elif completed == 'false':
        tasks_qs = [task for task in tasks_qs if not task.completed]
    
    # Today's tasks filter
    today_filter = request.GET.get('today', '')
    if today_filter == 'true':
        tasks_qs = [task for task in tasks_qs if task.is_due_today()]
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all().order_by('name')
    
    # Calculate enhanced stats
    total_tasks = len(tasks_qs)
    completed_tasks = len([task for task in tasks_qs if task.completed])
    overdue_tasks = len([task for task in tasks_qs if task.is_overdue()])
    today_tasks = len([task for task in tasks_qs if task.is_due_today()])
    
    context = {
        'tasks': tasks_qs,
        'q': query,
        'priority': priority,
        'category_value': category_name,
        'completed_value': completed,
        'today_filter': today_filter,
        'categories': categories,
        'now': timezone.now(),
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
    }
    return render(request, 'todo/index.html', context)

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
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

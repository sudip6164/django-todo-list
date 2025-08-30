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
    
    # Get only categories that have tasks (for filters)
    filter_categories = Category.objects.filter(task__isnull=False).distinct().order_by('name')
    
    # Get all categories (for bulk actions)
    all_categories = Category.objects.all().order_by('name')
    
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
        'categories': filter_categories,
        'all_categories': all_categories,
        'now': timezone.now(),
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
    }
    return render(request, 'todo/index.html', context)

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        notes = request.POST.get('notes', '')
        priority = request.POST.get('priority', 'M')
        category_name = request.POST.get('category', '').strip()
        due_date_str = request.POST.get('due_date', None)
        parent_task_id = request.POST.get('parent_task', '')

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M")

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        parent_task = None
        if parent_task_id:
            parent_task = Task.objects.filter(id=parent_task_id).first()

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date,
                priority=priority,
                description=description,
                notes=notes,
                category=category,
                parent_task=parent_task,
            )
        return redirect('index')

    # Get all tasks for parent task selection
    all_tasks = Task.objects.filter(completed=False).order_by('title')
    
    return render(request, 'todo/add.html', {'all_tasks': all_tasks})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        notes = request.POST.get('notes', '')
        priority = request.POST.get('priority', 'M')
        category_name = request.POST.get('category', '').strip()
        due_date_str = request.POST.get('due_date', None)
        parent_task_id = request.POST.get('parent_task', '')

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M")

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        parent_task = None
        if parent_task_id:
            parent_task = Task.objects.filter(id=parent_task_id).first()

        task.title = title or task.title
        task.description = description
        task.notes = notes
        task.priority = priority
        task.category = category
        task.due_date = due_date
        task.parent_task = parent_task
        task.save()
        return redirect('index')

    # Get all tasks for parent task selection (excluding self and completed tasks)
    all_tasks = Task.objects.filter(completed=False).exclude(id=task_id).order_by('title')
    
    return render(request, 'todo/edit.html', {
        'task': task,
        'all_tasks': all_tasks
    })

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def bulk_action(request):
    """Handle bulk actions on multiple tasks"""
    print(f"=== BULK ACTION VIEW CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Request POST data: {request.POST}")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        task_ids = request.POST.getlist('task_ids')
        
        print(f"Action: {action}")
        print(f"Task IDs: {task_ids}")
        
        if action and task_ids:
            tasks = Task.objects.filter(id__in=task_ids)
            print(f"Found {tasks.count()} tasks to update")
            
            if action == 'complete':
                tasks.update(completed=True)
                print(f"Marked {tasks.count()} tasks as complete")
            elif action == 'delete':
                deleted_count = tasks.count()
                tasks.delete()
                print(f"Deleted {deleted_count} tasks")
        else:
            print("No action or task_ids provided")
        
        print("Redirecting to index...")
        return redirect('index')
    else:
        print("Not a POST request, redirecting...")
        return redirect('index')

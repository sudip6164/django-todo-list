from .models import Task
from django.utils import timezone

def task_stats(request):
    """Make task statistics available on every page"""
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    
    # Calculate overdue and today's tasks
    now = timezone.now()
    overdue_tasks = Task.objects.filter(
        completed=False,
        due_date__lt=now
    ).count()
    
    today_tasks = Task.objects.filter(
        completed=False,
        due_date__date=now.date()
    ).count()
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
    }

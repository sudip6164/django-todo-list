from .models import Task

def task_stats(request):
    """Make task statistics available on every page"""
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }

#!/usr/bin/env python
import os
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from todo.models import Task

# Check all tasks with due dates
tasks_with_dates = Task.objects.filter(due_date__isnull=False)

print(f"Found {tasks_with_dates.count()} tasks with due dates")
print(f"Current time: {timezone.now()}")

for task in tasks_with_dates:
    print(f"\nTask: {task.title}")
    print(f"Due date: {task.due_date}")
    print(f"Is timezone aware: {task.due_date.tzinfo is not None}")
    print(f"Is overdue: {task.is_overdue()}")
    print(f"Due today: {task.is_due_today()}")
    
    # Fix timezone if needed
    if task.due_date.tzinfo is None:
        print("⚠️  Fixing timezone...")
        task.due_date = timezone.make_aware(task.due_date)
        task.save()
        print(f"✅ Fixed: {task.due_date}")
    else:
        print("✅ Already timezone aware")

from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['completed', '-priority', 'due_date', '-created_at']

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Check if task is overdue"""
        if self.completed or not self.due_date:
            return False
        return self.due_date < timezone.now()

    def is_due_today(self):
        """Check if task is due today"""
        if self.completed or not self.due_date:
            return False
        today = timezone.now().date()
        return self.due_date.date() == today

    def get_ordering_value(self):
        """Get value for smart ordering: overdue first, then due today, then by due date"""
        if self.completed:
            return 999  # Completed tasks go last
        if not self.due_date:
            return 998  # No due date tasks go second to last
        
        now = timezone.now()
        if self.due_date < now:
            return 0  # Overdue tasks first
        elif self.due_date.date() == now.date():
            return 1  # Due today tasks second
        else:
            return 2  # Future tasks by due date

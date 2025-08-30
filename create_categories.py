#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from todo.models import Category

# Default categories
default_categories = [
    'Work',
    'Personal',
    'Shopping',
    'Health',
    'Study',
    'Home',
    'Finance',
    'Travel'
]

# Create categories if they don't exist
for category_name in default_categories:
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        print(f"Created category: {category_name}")
    else:
        print(f"Category already exists: {category_name}")

print(f"\nTotal categories in database: {Category.objects.count()}")

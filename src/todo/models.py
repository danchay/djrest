from django.db import models

# This class will more or less map to a table in the db
class ToDoList(models.Model):
    """A model for representing single line items in a todo list"""
    # Defines a required text field of 100 characters.
    title = models.CharField(max_length=100)

class ToDoListItem(models.Model):
    # Define a model to represent a single line item in a todo list
    # The parent will be able to access its items with the related_name
    # 'items': When a parent is deleted, this will be deleted too.
    todo_list = models.ForeignKey(
        'ToDoList',
        related_name='items',
        on_delete=models.CASCADE
    )

    # This defines a required title of not more than 100 char
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

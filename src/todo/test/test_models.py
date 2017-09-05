from django.test import TestCase
from todo.models import ToDoList, ToDoListItem

class ToDoTestCase(TestCase):

    def to_do_list(self):
        # Create a todo list object to db
        ToDoList.objects.create(title="Test List")
        # Verify that object was saved
        todo_list = ToDoList.objects.get(title="Test List")
        # Verify data is exists and is accurate
        self.assertEqual(todo_list.title, "Test List")
        # Delete the list
        todo_list.delete()
        # Try to retrieve the todo list and ensure it's not there
        try:
            retrieved_list = ToDoList.objects.get(title="Test List")
        # Catch the DoesNotExist error we're hoping to get
        except ToDoList.DoesNotExist:
            retrieved_list = None
        self.assertEqual(retrieved_list, None)

    # Test to verify items function
    def test_todo_list_items(self):
        """
        This test creates a todo list, adds an item to it,
        verifies that the item is accessible through the 'items'
        related name. Then it deletes everything.
        """
        todo_list = ToDoList.objects.create(title="Test")
        todo_list_item = ToDoListItem.objects.create(
            todo_list = todo_list,
            title="Test Item",
            description="This is a test todo list item")

        # Verify that the related name returns the todo_list item
        self.assertEqual(todo_list.items.count(), 1)
        self.assertEqual(todo_list.items.first(), todo_list_item)

        # Delete the list. Should also delete items in list.
        todo_list.delete()

        # Verify the todo list item was deleted with the list due to
        # the CASCADED attribute we gave our model
        try:
            retrieved_item = ToDoListItem.objects.get(title="Test Item")
        except ToDoListItem.DoesNotExist:
            retrieved_item = None
        self.assertEqual(retrieved_item, None)

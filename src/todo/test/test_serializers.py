from django.test import TestCase
from todo.serializers import serializers

class ToDoListTestCase(TestCase):

    def test_todo_list_create(self):
        """
        Define some json data we expect to receive and use the
        serializer to parse it into models. Test he models to
        make sure they're correct.
        """
        # Define dat that resembles what would come through the api
        # A python dictionary often is what JSON data is parsed into initially.
        data = {
            'title': 'Test List',
            'items': [
                {
                    'title': 'Test Item 1',
                    'description': 'This is test item 1'
                },
                {
                    'title': 'Test Item 2',
                    'description': 'This is test item 2'
                }
            ]
        }

        # Pass the data into the serializer for parsing.
        serializer = serializers.ToDoList(data=data)

        # Verify that the serializer thinks the data is valid.
        self.assertTrue(serializer.is_valid())

        # Get the object parsed from the serializer
        todo_list = serializer.save()

        # Verify the title is correct
        self.assertEqual(todo_list.title, 'Test List')

        # Verify that it has two items.
        self.assertEqual(todo_list.items.count(), 2)

import json
from django.test import TestCase, Client
from todo import models

class ToDoListTestCase(TestCase):
    """ Tests for the todo list models """

    def setUp(self):
        """ Initialize the TestCae with a test client """
        self.client=Client()
        self.test_list = models.ToDoList.objects.create(title='Test ToDo List')
        super(ToDoListTestCase, self).setUp()

    def test_todo_list_item_post_delete(self):
        """
        Test the /todo_list/items POST method to add items and the /todo_list/items DELETE method to remove todo list items.
        """
        # Define the data to post
        post_data = {
            "title": "Test List Item",
            "description": "This is a test."
        }

        # Post a new ToDoListItem
        response = self.client.post(
            '/todo_lists/{0}/items'.format(self.test_list.id),
            json.dumps(post_data),
            content_type='application/json')

        # Always check the response status code
        self.assertEqual(response.status_code, 200)

        # Get the id of the saved object we posted
        list_item_id = response.data['id']

        # Try to delete that item
        response = self.client.delete('/todo_lists/items/{0}'.format(list_item_id))

        # Verify the response we got is a 204 no content
        self.assertEqual(response.status_code, 204)

    def test_todo_list_get_post_delete(self):
        """
        Test the /todo_lists GET POST and DElETE methods.
        """
        # Define data in a dictionary to post to the API
        post_data = {
            "title": "Test List",
            "items": [
                {
                "title": "Test Item 1",
                "description": "This is test item 1"
                },
                {
                "title": "Test Item 2",
                "description": "This is test item 2"
                }
            ]
        }

        # Try to post the data as json
        response = self.client.post('/todo_lists',
            json.dumps(post_data),
            content_type="application/json")

        # Always assert that your status code is as expected
        self.assertEqual(response.status_code, 200)

        # Get the todo list id from the response
        todo_list_id = response.data['id']

        # Retrieve all the todo lists
        response = self.client.get('/todo_lists')
        self.assertEqual(response.status_code, 200)

        # Get the todo lists from the endpoint
        received_todos = response.data

        # Search for the todo list we posted
        is_present = False
        found_list = None
        for received_todo_list in received_todos:
            if received_todo_list['id'] == todo_list_id:
                is_present = True
                found_list = received_todo_list
                break

        # Assert that the list we posted was indeed found
        self.assertTrue(is_present)

        # Verify the list title is correct
        self.assertEqual(found_list['title'], post_data['title'])

        # Verify the length of the items list is correct
        self.assertEqual(len(found_list['items']), len(post_data['items']))

        # For each ToDoListItem verify its data is correct
        for i in range(0, len(found_list['items'])):
            found = found_list['items'][i]
            expected = post_data['items'][i]
            self.assertEqual(found['title'], expected['title'])
            self.assertEqual(found['description'], expected['description'])

        # Delete the todo list
        response = self.client.delete('/todo_lists/{0}'.format(todo_list_id))

        # Verify we get a 204 HTTP No Content Response
        self.assertEqual(response.status_code, 204)

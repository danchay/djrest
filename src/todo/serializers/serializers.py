from rest_framework import serializers
from todo import models

class ToDoListItem(serializers.ModelSerializer):
    """
    Create the first serializer for ToDoListItems
    This is a model serializer, so it will autogenerate a
    full serializer from the model.
    """
    class Meta:
        # Specify the model to use
        model = models.ToDoListItem
        # Specify the field names to show in the api
        fields = ('id', 'todo_list_id', 'title', 'description')

class ToDoList(serializers.ModelSerializer):
    """
    Create a second serializer for the ToDoList model.
    This will nest the ToDoListItem serializer within it.
    """
    items = ToDoListItem(many=True)

    class Meta:
        model = models.ToDoList
        # Specify the fields from ToDoList that we want the api to
        # return/consume
        fields = ('id', 'title', 'items')

    def create(self, validated_data):
        """
        Override the default create method so that we can serialize
        whole ToDoList objects with ToDoListItems.

        :param validated_data: A Dictionary of values to use for object creation
        :type validated_data: OrderedDict
        :returns ToDoList: A ToDoList model object
        """
        # Remove the value of items from the ToDoList validated data. We'll use this later
        items_data = validated_data.pop('items')

        # Create a new ToDoList with the validated data passed in.
        todo_list = models.ToDoList.objects.create(**validated_data)

        # For each item in the 'items' validated data
        for item_data in items_data:
            # Modify its validated data to reference the ToDoList we just made
            item_data['todo_list_id'] = todo_list.id
            # Create the ToDoListItem with the item data
            models.ToDoListItem.objects.create(**item_data)

        # Return the new todo_list
        return todo_list


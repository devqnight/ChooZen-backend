from choozen.models import Movie
from rest_framework.serializers import ModelSerializer

# to convert a model to json format (serialize)

class MovieSerializer(ModelSerializer):

    # example to show how to rename fields returned by the api
    # in the db, the field name is "due_date" and when you call the api, it will be called "dueDate"
    # dueDate = serializers.DateField(source='due_date')

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['due_date'] otherwise you will get the due_date field in the json

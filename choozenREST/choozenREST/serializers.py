from select import select
from django.db.models import fields
from rest_framework import serializers
from choozen.models import Movie, Genre, GroupList, IsPartOf, User, Person
from rest_framework.serializers import ModelSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

# to convert a model to json format (serialize)

class MovieSerializer(ModelSerializer):
    imdb_id = serializers.CharField(max_length=10, required=True)
    # example to show how to rename fields returned by the api
    # in the db, the field name is "due_date" and when you call the api, it will be called "dueDate"
    # dueDate = serializers.DateField(source='due_date')

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['due_date'] otherwise you will get the due_date field in the json

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CustomRegisterSerializer(RegisterSerializer):
    birthdate = serializers.DateField(required=True)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'birthdate')

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['birthdate'] = self.validated_data.get('birthdate', '')
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        return data_dict

class CustomUserDetailsSerializer(ModelSerializer):
    class Meta(UserDetailsSerializer):
      fields = UserDetailsSerializer.Meta.fields + ('birthdate',)

class GroupUserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class CustomGenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class CustomGroupListSerializer(ModelSerializer):
    class Meta:
        model = GroupList
        fields = '__all__'

class CustomIsPartOfSerializer(ModelSerializer):
    class Meta:
        model = IsPartOf
        fields = '__all__'

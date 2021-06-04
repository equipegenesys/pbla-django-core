from django.contrib.auth.models import User, Group
from .models import Equipe, Turma
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['tag_turma', 'user']
        # list_serializer_class = TurmaUserSerializer

class IntegrantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['user']

# class TurmaUserSerializer(serializers.ListSerializer):
#     class Meta:
#         model = Turma
#         # fields = ['id', 'user_id', 'turma_id']
#         fields = ['id', 'tag_turma']
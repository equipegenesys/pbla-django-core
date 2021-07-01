from django.contrib.auth.models import User, Group
from . import models
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
        model = models.Turma
        fields = ['tag_turma', 'user']
        # list_serializer_class = TurmaUserSerializer

class IntegrantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipe
        fields = ['user']

# class TurmaUserSerializer(serializers.ListSerializer):
#     class Meta:
#         model = Turma
#         # fields = ['id', 'user_id', 'turma_id']
#         fields = ['id', 'tag_turma']


class UserIntegSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserIntegBridge
        fields = ['pessoa', 'integracao', 'is_active']
    def create(self, validated_data):
        obj, created = models.UserIntegBridge.objects.update_or_create(
                        pessoa_id = self.validated_data['pessoa'].pk, 
                        integracao_id = self.validated_data['integracao'].pk,
                        defaults={'is_active': True},
                        )
        return obj

class EquipeIntegSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EquipeIntegBridge
        fields = ['equipe', 'integracao', 'is_active']
    def create(self, validated_data):
        obj, created = models.EquipeIntegBridge.objects.update_or_create(
                        equipe_id = self.validated_data['equipe'].pk, 
                        integracao_id = self.validated_data['integracao'].pk,
                        defaults={'is_active': True},
                        )
        return obj

class InstituicaoIntegSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstituicaoIntegBridge
        fields = ['instituicao', 'integracao', 'is_active']
    def create(self, validated_data):
        obj, created = models.InstituicaoIntegBridge.objects.update_or_create(
                        instituicao_id = self.validated_data['instituicao'].pk, 
                        integracao_id = self.validated_data['integracao'].pk,
                        defaults={'is_active': True},
                        )
        return obj
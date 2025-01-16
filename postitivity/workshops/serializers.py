from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer
# from users.models import CustomUser


class NoteSerializer(serializers.ModelSerializer):

    supporter = CustomUserSerializer(many = False, read_only=True)
    class Meta:
        model = apps.get_model('projects.Pledge')
        fields = '__all__'



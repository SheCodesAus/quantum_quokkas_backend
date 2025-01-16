from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer



class NoteSerializer(serializers.ModelSerializer):
    added_by_user = CustomUserSerializer(many = False, read_only=True)
    class Meta:
        model = apps.get_model('workshops.Notes')
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    organisation_workshops = CustomUserSerializer(many = False, read_only=True)
    members = CustomUserSerializer(source = 'members', many=True, read_only=True)
    class Meta:
        model = apps.get_model('workshop.Organisation')
        fields = ('id', 'organisation_name', 'organisation_workshops', 'members','added_date', 'added_by_user', 'is_archived')
        exta_kwargs = {'members': {'required': False},
                       'organisation_workshops': {'required': False}}

class WorkshopSerializer(serializers.ModelSerializer):  
    notes = NoteSerializer(many=True, read_only=True)
    organisation = OrganisationSerializer(source = 'organisation', many = False, read_only=True)
    owner = CustomUserSerializer(source = 'created_by_user', many=False, read_only= True)
    class Meta:
        model = apps.get_model('workshops.Workshop')
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'image_url', 'date_created', 'owner', 'location', 'category', 'coding_language', 'organisation','is_archived', 'archive_details')


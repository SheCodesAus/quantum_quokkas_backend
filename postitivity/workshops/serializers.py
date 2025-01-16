from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class NoteSerializer(serializers.ModelSerializer):

    added_by_user = CustomUserSerializer(many = False, read_only=True)
    class Meta:
        model = apps.get_model('workshops.Notes')
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    club_owner = CustomUserSerializer(many = False, read_only=True)
    members = CustomUserSerializer(source = 'club_members', many=True, read_only=True)
    sport_id = SportsSerializer(source = 'sport', many=False, read_only=True)
    class Meta:
        model = apps.get_model('projects.Sportsclub')
        fields = ('id', 'club_owner', 'club', 'description', 'club_size', 'club_location', 'is_active', 'club_logo', 'sport_id', 'sport', 'club_members', 'members')
        exta_kwargs = {'club_members': {'required': False}}

class WorkshopSerializer(serializers.ModelSerializer):
    
    notes = NoteSerializerSerializer(many=True, read_only=True)
    organisation = ClubsSerializer(source = 'owner_club', many = False, read_only=True)
    class Meta:
        model = apps.get_model('projects.Project')
        fields = ('id', 'title', 'description', 'goal', 'image', 'fund_type', 'is_open', 'date_created', 'end_date', 'member_only', 'club','owner_club', 'pledges')


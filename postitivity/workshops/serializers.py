from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer

# Basic serializers for our core models
class CohortSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Cohorts')
       fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Location')
       fields = '__all__'

class NoteCategorySerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Note_category')
       fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Category')
       fields = '__all__'

class ArchiveSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Archive_details')
       fields = '__all__'

class CodingLanguageSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Coding_language')
       fields = '__all__'

class OrganisationSerializer(serializers.ModelSerializer):
   organisation_workshops = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   members = CustomUserSerializer(source = 'members', many=True, read_only=True)
   added_by_user = CustomUserSerializer(many=False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Organisation')
       fields = ('id', 'organisation_name', 'organisation_workshops', 'members',
                'added_date', 'added_by_user', 'is_archived')
       extra_kwargs = {
           'members': {'required': False},
           'organisation_workshops': {'required': False}
       }

#making a base serializer for workshops so we can pull workshop details in notes
class WorkshopBaseSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(many=False, read_only=True)  # Removed source='organisation'
    archive_details = ArchiveSerializer(many=False, read_only=True)    # Removed source='archive_details'
    location = LocationSerializer(many=False, read_only=True)          # Removed source='location'
    category = CategorySerializer(many=False, read_only=True)          # Removed source='category'
    owner = CustomUserSerializer(source='created_by_user', many=False, read_only=True)  # Kept this one since it maps to a different name
    coding_language = CodingLanguageSerializer(many=False, read_only=True)  # Removed source='coding_language'
    
    class Meta:
        model = apps.get_model('workshops.Workshop')
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 
                 'image_url', 'date_created', 'owner', 'location', 'category', 
                 'coding_language', 'organisation', 'is_archived', 'archive_details')
        # Location is required, everything else optional
        extra_kwargs = {
            'category': {'required': False},
            'coding_language': {'required': False},
            'organisation': {'required': False},
            'archive_details': {'required': False},
        }

#use base workshop serializer in notes to pull workshop details
class NoteSerializer(serializers.ModelSerializer):
    added_by_user = CustomUserSerializer(many=False, read_only=True)
    user = CustomUserSerializer(many=False, read_only=True)
    note_category = NoteCategorySerializer(many=False, read_only=True)
    archive_details = ArchiveSerializer(many=False, read_only=True)
    coding_language = CodingLanguageSerializer(many=False, read_only=True)
    workshop = WorkshopBaseSerializer(many=False, read_only=True)
    
    class Meta:
        model = apps.get_model('workshops.Notes')
        fields = '__all__'
        extra_kwargs = {
            'note_category': {'required': False},
            'coding_language': {'required': False},
            'archive_details': {'required': False},
            'workshop': {'required': True} #required in jSON when creating a new note
        }


#make a workshopserializer using the base serializer and add notes details
class WorkshopSerializer(WorkshopBaseSerializer):
   notes = NoteSerializer(many=True, read_only=True)

   class Meta(WorkshopBaseSerializer.Meta):
       fields = WorkshopBaseSerializer.Meta.fields + ('notes',)

class WorkshopDetailSerializer(WorkshopSerializer):
   def update(self, instance, validated_data):
       instance.title = validated_data.get('title', instance.title)
       instance.description = validated_data.get('description', instance.description)
       instance.start_date = validated_data.get('start_date', instance.start_date)
       instance.end_date = validated_data.get('end_date', instance.end_date)
       instance.image_url = validated_data.get('image_url', instance.image_url)
       instance.location = validated_data.get('location', instance.location)      
       instance.category = validated_data.get('category', instance.category)
       instance.coding_language = validated_data.get('coding_language', instance.coding_language)      
       instance.organisation = validated_data.get('organisation', instance.organisation)
       instance.is_archived = validated_data.get('is_archived', instance.is_archived)
       instance.archive_details = validated_data.get('archive_details', instance.archive_details)
       instance.save()
       return instance

class NoteDetailSerializer(NoteSerializer):
   workshop = WorkshopDetailSerializer(many=False, read_only=True)
   
   def update(self, instance, validated_data):
       instance.content = validated_data.get('content', instance.content)
       instance.workshop = validated_data.get('workshop', instance.workshop)
       instance.user = validated_data.get('user', instance.user)
       instance.anonymous = validated_data.get('anonymous', instance.anonymous)
       instance.note_category = validated_data.get('note_category', instance.note_category)
       instance.coding_language = validated_data.get('coding_language', instance.coding_language)
       instance.likes_count = validated_data.get('likes_count', instance.likes_count)
       instance.is_archived = validated_data.get('is_archived', instance.is_archived)
       instance.archive_details = validated_data.get('archive_details', instance.archive_details)
       instance.save()
       return instance    
   
class OrganisationDetailSerializer(OrganisationSerializer):
   def update(self, instance, validated_data):
       instance.organisation_name = validated_data.get('organisation_name', instance.organisation_name)
       instance.is_archived = validated_data.get('is_archived', instance.is_archived)
       instance.save()
       return instance
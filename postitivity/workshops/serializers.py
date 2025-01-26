from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer, CustomUserBriefSerializer

# Basic serializers for our core models
class CohortSerializer(serializers.ModelSerializer):

   class Meta:
       model = apps.get_model('workshops.Cohorts')
       fields = ('id', 'cohort_name')

class LocationSerializer(serializers.ModelSerializer):

   class Meta:
       model = apps.get_model('workshops.Location')
       fields = ('id', 'location')

class NoteCategorySerializer(serializers.ModelSerializer):

   class Meta:
       model = apps.get_model('workshops.Note_category')
       fields = ('id', 'note_category_name')

class CategorySerializer(serializers.ModelSerializer):

   class Meta:
       model = apps.get_model('workshops.Category')
       fields = ('id', 'category_name')


class CodingLanguageSerializer(serializers.ModelSerializer):

   class Meta:
       model = apps.get_model('workshops.Coding_language')
       fields = ('id', 'language')

class OrganisationSerializer(serializers.ModelSerializer):
   class Meta:
       model = apps.get_model('workshops.Organisation')
       fields = ('id', 'organisation_name', 'is_archived')


#making a base serializer for workshops so we can pull workshop details in notes
class WorkshopBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('workshops.Workshop')
        fields = ('id', 'title')
      

#use base workshop serializer in notes to pull workshop details
class NoteSerializer(serializers.ModelSerializer):
    added_by_user = CustomUserBriefSerializer(many=False, read_only=True)
    user = CustomUserBriefSerializer(many=False, read_only=True)
    archive_user = CustomUserBriefSerializer(many=False, read_only=True)
    workshop_id = WorkshopBaseSerializer(source = 'workshop', many=False, read_only=True)
    class Meta:
        model = apps.get_model('workshops.Notes')
        fields = ('id','added_by_user','user','content','workshop', 'workshop_id', 'likes_count', 'anonymous','date_created','is_archived','archive_reason','archive_user')
        extra_kwargs = {
            'workshop': {'required': True}, #required in jSON when creating a new note
            'archive_reason' : {'required': False, 'allow_blank': True, 'allow_null': True},
            'archive_user': {'required': False, 'read_only': True}
        }

#make a workshopserializer using the base serializer and add notes details
class WorkshopSerializer(WorkshopBaseSerializer):
    organisation_id = OrganisationSerializer(source = 'organisation', many=False, read_only=True)  
    location_id = LocationSerializer( source = 'location', many=False, read_only=True)              
    owner = CustomUserBriefSerializer(source='created_by_user', many=False, read_only=True) 
    archive_user = CustomUserBriefSerializer(many=False, read_only=True)
    class Meta:
        model = apps.get_model('workshops.Workshop')
        fields = WorkshopBaseSerializer.Meta.fields + ('description', 'start_date', 'end_date', 'date_created', 'owner', 'location', 
                                                       'location_id', 'organisation', 'organisation_id', 'is_archived', 'archive_reason','archive_user')
            # Location is required, everything else optional
        extra_kwargs = {
            'organisation': {'required': False},
            'archive_reason': {'required': False},
            'archive_user': {'required': False},
        }

class WorkshopDetailSerializer(WorkshopSerializer):
    def validate(self, data):
        if data.get('is_archived') == 1 and not data.get('archive_reason'):
            raise serializers.ValidationError(
                {'archive_reason': 'Archive reason is required when archiving'}
            )
        return data

    def update(self, instance, validated_data):
        if validated_data.get('is_archived') == 1 and instance.is_archived == 0:
            validated_data['archive_user'] = self.context['request'].user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class NoteDetailSerializer(NoteSerializer):
    workshop = WorkshopBaseSerializer(many=False, read_only=True)
   
    def validate(self, data):
        if data.get('is_archived') == 1 and not data.get('archive_reason'):
            raise serializers.ValidationError({
                'archive_reason': 'Archive reason is required when archiving'
            })
        return data

    def update(self, instance, validated_data):
        if validated_data.get('is_archived') == 1 and instance.is_archived == 0:
            validated_data['archive_user'] = self.context['request'].user
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
   
class OrganisationDetailSerializer(OrganisationSerializer):
   def update(self, instance, validated_data):
       instance.organisation_name = validated_data.get('organisation_name', instance.organisation_name)
       instance.is_archived = validated_data.get('is_archived', instance.is_archived)
       instance.save()
       return instance
   
class LocationDetailSerializer(LocationSerializer):
   def update(self, instance, validated_data):
       instance.location = validated_data.get('location', instance.organisation_name)
       instance.is_archived = validated_data.get('is_archived', instance.is_archived)
       instance.save()
       return instance   
      
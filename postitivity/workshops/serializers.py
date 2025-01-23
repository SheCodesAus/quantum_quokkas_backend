from rest_framework import serializers
from django.apps import apps
from users.serializers import CustomUserSerializer

# Basic serializers for our core models
class CohortSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Cohorts')
       fields = ('id', 'cohort_name','added_by_user')

class LocationSerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Location')
       fields = ('id', 'location','added_by_user')

class NoteCategorySerializer(serializers.ModelSerializer):
   added_by_user = CustomUserSerializer(many = False, read_only=True)
   class Meta:
       model = apps.get_model('workshops.Note_category')
       fields = ('id', 'organisation_name','added_by_user')

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
   members = CustomUserSerializer(many=True, read_only=True) #deleted source
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
    #changed these to map to _id as it is the only way to return all information on a foreign key (other methods will only return the 'id')
    organisation_id = OrganisationSerializer(source = 'organisation', many=False, read_only=True)  
    location_id = LocationSerializer( source = 'location', many=False, read_only=True)       
    category_id = CategorySerializer(source = 'category', many=False, read_only=True)         
    owner = CustomUserSerializer(source='created_by_user', many=False, read_only=True) 
    coding_language_id = CodingLanguageSerializer(source = 'coding_language', many=False, read_only=True)  
    archive_user = CustomUserSerializer(many=False, read_only=True)
    
    class Meta:
        model = apps.get_model('workshops.Workshop')
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 
                 'image_url', 'date_created', 'owner', 'location', 'location_id', 'category', 'category_id',
                 'coding_language', 'coding_language_id','organisation', 'organisation_id', 'is_archived', 'archive_reason','archive_user')
        # Location is required, everything else optional
        extra_kwargs = {
            'category': {'required': False},
            'coding_language': {'required': False},
            'organisation': {'required': False},
            'archive_reason': {'required': False},
            'archive_user': {'required': False},
        }

#use base workshop serializer in notes to pull workshop details
class NoteSerializer(serializers.ModelSerializer):
    added_by_user = CustomUserSerializer(many=False, read_only=True)
    user = CustomUserSerializer(many=False, read_only=True)
    note_category = NoteCategorySerializer(many=False, read_only=True)
    coding_language = CodingLanguageSerializer(many=False, read_only=True)
    workshop = WorkshopBaseSerializer(many=False, read_only=True)
    archive_user = CustomUserSerializer(many=False, read_only=True)

    class Meta:
        model = apps.get_model('workshops.Notes')
        fields = '__all__'
        extra_kwargs = {
            'note_category': {'required': False},
            'coding_language': {'required': False},
            'workshop': {'required': True}, #required in jSON when creating a new note
            'archive_reason' : {'required': False, 'allow_blank': True, 'allow_null': True},
            'archive_user': {'required': False, 'read_only': True}
        }


#make a workshopserializer using the base serializer and add notes details
class WorkshopSerializer(WorkshopBaseSerializer):
   notes = NoteSerializer(many=True, read_only=True)

   class Meta(WorkshopBaseSerializer.Meta):
       fields = WorkshopBaseSerializer.Meta.fields + ('notes',)

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
    workshop = WorkshopDetailSerializer(many=False, read_only=True)
   
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
   
class ArchiveDetailSerializer(ArchiveSerializer):
   def update(self, instance, validated_data):
       instance.archive_table = validated_data.get('location', instance.archive_table)
       instance.archive_reason = validated_data.get('is_archived', instance.archive_reason)
       instance.save()
       return instance      
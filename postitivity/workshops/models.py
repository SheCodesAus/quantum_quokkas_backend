from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Location(models.Model):
   location = models.CharField(max_length=50, unique=True)
   created_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_locations'
    )
   is_archived = models.BooleanField(default=0)

class Cohorts(models.Model):
   cohort_name = models.CharField(max_length=50, unique=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_cohorts'
    )
   created_date = models.DateTimeField(auto_now_add=True)
   is_archived = models.BooleanField(default=0)


class Note_category(models.Model):
   note_category_name = models.CharField(max_length=50, unique=True)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_note_categories'
    )
   is_archived = models.BooleanField(default=0)

class Category(models.Model):
   category_name = models.CharField(max_length=50, unique=True)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user =models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_categories'
    )
   is_archived = models.BooleanField(default=0)  

class Coding_language(models.Model):
   language = models.CharField(max_length=50, unique=True)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_languages'
    )
   is_archived = models.BooleanField(default=0)  


class Organisation(models.Model):
   organisation_name = models.CharField(max_length=100, unique=True)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='added_organisation'
    )
   is_archived = models.BooleanField(default=0)     

class Workshop(models.Model):
   title = models.CharField(max_length=220)
   description = models.CharField(max_length=1000)
   start_date = models.DateTimeField()
   end_date = models.DateTimeField()
   image_url = models.URLField(max_length=2000, null=True, blank=True)
   date_created = models.DateTimeField(auto_now_add=True)
   created_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_workshops'
    )
   location = models.ForeignKey(
        'Location',
         on_delete=models.CASCADE,
         related_name='category_workshops',
         null=True, blank=True)
   category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='workshops',
        null=True, blank=True
    )      
   coding_language = models.ForeignKey(
        'Coding_language',
         on_delete=models.CASCADE,
         related_name='language_workshops',
         null=True, blank=True)
   organisation = models.ForeignKey(
        'Organisation',
         on_delete=models.CASCADE,
         related_name='organisation_workshops',
         null=True, blank=True)
   is_archived = models.BooleanField(default=0)
   archive_reason = models.CharField(max_length=220, null=True, blank=True)
   archive_user = models.ForeignKey(
         get_user_model(),
         on_delete=models.CASCADE,
         related_name='archived_workshops',
         null=True, blank=True)

class Notes(models.Model):
   content = models.CharField(max_length=220)
   user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_notes'
    )
   workshop = models.ForeignKey(
      'Workshop',
      on_delete = models.CASCADE,
      related_name= 'notes'
   )
   anonymous = models.BooleanField(default=0)
   date_created = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='added_notes'
    )
   note_category = models.ForeignKey(
        'Note_category',
        on_delete=models.CASCADE,
        related_name='cat_notes',
        null=True, blank=True
    )      
   coding_language = models.ForeignKey(
        'Coding_language',
         on_delete=models.CASCADE,
         related_name='language_notes',
         null=True, blank=True)
   likes_count = models.IntegerField(default=0)
   is_archived = models.BooleanField(default=0)
   archive_reason = models.CharField(max_length=220, null=True, blank=True)
   archive_user = models.ForeignKey(
         get_user_model(),
         on_delete=models.CASCADE,
         related_name='archived_notes',
         null=True, blank=True)
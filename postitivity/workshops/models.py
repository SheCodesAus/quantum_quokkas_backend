from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Location(models.Model):
   location = models.CharField(max_length=50)
   created_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_locations'
    )
   is_archived = models.BooleanField()

class Cohorts(models.Model):
   cohort_name = models.CharField(max_length=50)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_cohorts'
    )
   created_date = models.DateTimeField(auto_now_add=True)
   is_archived = models.BooleanField()

class Archive_details(models.Model):
   archive_table = models.CharField(max_length=50)
   archive_date = models.DateTimeField(auto_now_add=True)
   archive_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='archived_items'
    )
   archive_reason = models.CharField(max_length=220)

class Note_category(models.Model):
   note_category_name = models.CharField(max_length=50)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_note_categories'
    )
   is_archived = models.BooleanField()

class Category(models.Model):
   category_name = models.CharField(max_length=50)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user =models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_categories'
    )
   is_archived = models.BooleanField()  

class Coding_language(models.Model):
   language = models.CharField(max_length=50)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_languages'
    )
   is_archived = models.BooleanField()  


class Organisation(models.Model):
   organisation_name = models.CharField(max_length=100)
   added_date = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='added_organisation'
    )
   is_archived = models.BooleanField()     

class Workshop(models.Model):
   title = models.CharField(max_length=220)
   description = models.CharField(max_length=1000)
   start_date = models.DateTimeField()
   end_date = models.DateTimeField()
   image_url = models.URLField(max_length=2000)
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
   is_archived = models.BooleanField()
   archive_id = models.ForeignKey(
        'Archive_details',
         on_delete=models.CASCADE,
         related_name='archived_workshops',
         null=True, blank=True)

class Notes(models.Model):
   content = models.CharField(max_length=220)
   user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_notes'
    )
   anonymous = models.BooleanField()
   date_created = models.DateTimeField(auto_now_add=True)
   added_by_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='added_notes'
    )
   note_category = models.ForeignKey(
        'Note_category',
        on_delete=models.CASCADE,
        related_name='notes',
        null=True, blank=True
    )      
   coding_language = models.ForeignKey(
        'Coding_language',
         on_delete=models.CASCADE,
         related_name='language_notes',
         null=True, blank=True)
   likes_count = models.IntegerField()
   is_archived = models.BooleanField()
   archive_id = models.ForeignKey(
        'Archive_details',
         on_delete=models.CASCADE,
         related_name='archived_notes',
         null=True, blank=True)

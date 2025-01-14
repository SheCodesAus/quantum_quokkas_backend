from django.db import models

# Create your models here.
class Workshop(models.Model):
   title = models.CharField(max_length=200)
   start_date = models.DateTimeField()
   end_date = models.DateTimeField()
   category = models.IntegerField(null=True, blank=True)
   image_url = models.URLField()
   date_created = models.DateTimeField(auto_now_add=True)
   created_by_user = models.IntegerField()
   location = models.IntegerField(null=True, blank=True)
   coding_language = models.IntegerField(null=True, blank=True)
   organisation = models.IntegerField(null=True, blank=True)
   is_archived = models.BooleanField()
   archive_id = models.IntegerField(null=True, blank=True)

class Notes(models.Model):
   content = models.CharField(max_length=200)
   user_id = models.IntegerField()
   anonymous = models.BooleanField()
   date_created = models.DateTimeField(auto_now_add=True)
   added_by_user = models.IntegerField()
   note_category = models.IntegerField(null=True, blank=True)
   coding_language = models.IntegerField(null=True, blank=True)
   likes_count = models.IntegerField(default=0)
   is_archived = models.BooleanField()
   archive_id = models.IntegerField(null=True, blank=True)
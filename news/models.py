from django.db import models
from django.db.models import SET_DEFAULT


# Create your models here.
class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_trust_rating = models.IntegerField(default=0)
    source_name = models.TextField()

    def __str__(self):
        return self.source_name


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_source_id = models.TextField()
    content_headline = models.TextField()
    content_source = models.TextField()
    content_url = models.TextField()
    content_category = models.TextField()
    content_text = models.TextField()
    content_image = models.TextField()
    content_date = models.TextField()

    def __str__(self):
        return self.content_headline


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_label = models.TextField()
    category_code = models.TextField()

    def __str__(self):
        return self.category_label


class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    content_id = models.TextField()
    thread_response = models.TextField(max_length=300)

    def __str__(self):
        return self.content_id

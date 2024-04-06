from django.db import models


# Create your models here.
class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_trust_rating = models.IntegerField(default=0)
    source_name = models.TextField(max_length=50)

    def __str__(self):
        return self.source_name


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_source_id = models.IntegerField()
    content_headline = models.TextField(max_length=300)
    content_source = models.TextField(max_length=50)
    content_url = models.TextField(max_length=400)
    content_category = models.TextField(max_length=50)
    content_text = models.TextField(max_length=500)
    content_image = models.TextField(max_length=500)
    content_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content_headline


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_label = models.TextField(max_length=50)
    category_code = models.TextField(max_length=10, unique=True)

    def __str__(self):
        return self.category_label


class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    content_id = models.IntegerField()
    thread_response = models.TextField(max_length=300)

    def __str__(self):
        return self.content_id

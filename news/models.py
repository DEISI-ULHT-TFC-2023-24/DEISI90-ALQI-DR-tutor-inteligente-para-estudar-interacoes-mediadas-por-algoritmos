from django.db import models
from django.db.models import SET_DEFAULT


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_url = models.URLField(default="")
    source_trust_rating = models.IntegerField(default=0)
    source_name = models.TextField(unique=True)

    def __str__(self):
        return self.source_name


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_source_id = models.TextField()
    content_headline = models.TextField(unique=True)
    content_source = models.TextField()
    content_url = models.TextField()
    content_category = models.TextField()
    content_text = models.TextField()
    content_image = models.TextField()
    content_date = models.TextField()

    def __str__(self):
        return self.content_headline


class Category(models.Model):
    category_label = models.TextField(primary_key=True, unique=True)
    category_id = models.TextField()
    category_code = models.TextField()

    def __str__(self):
        return self.category_label


class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    content_id = models.IntegerField()
    content_title = models.TextField()
    thread_snippet = models.BinaryField()  #BLOB (group of snippets)

    def __str__(self):
        return self.content_title


class Snippet(models.Model):
    snippet_id = models.AutoField(primary_key=True)
    thread_id = models.IntegerField()
    snippet_text = models.TextField()
    snippet_options = models.BinaryField()  #BLOB (group of options)
    time_to_consume = models.IntegerField()
    type = models.TextField()
    sentiment_valence = models.TextField()
    sentiment_arousal = models.TextField()
    style = models.TextField()
    tone = models.TextField()

    def __str__(self):
        return self.snippet_text


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    snippet_id = models.IntegerField()
    option_default = models.TextField()
    option_added = models.BinaryField()

    def __str__(self):
        return self.option_id

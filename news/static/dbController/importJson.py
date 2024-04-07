from news.models import Source, Thread, Content, Category
import json
from django.db import connection


def import_json_data_RTP(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        # Prepare the data for the content instance
        content_data = {
            'content_source_id': 1,
            'content_source': 'RTP',
            'content_headline': news_item['headline'],
            'content_url': news_item['url'],
            'content_category': news_item['category'],
            'content_text': news_item['content'][0]['data'],
            'content_image': news_item['content'][1]['data'],
            'content_date': news_item['published']
        }

        # Update or create the content instance
        Content.objects.update_or_create(
            content_headline=news_item['headline'],  # Assuming headline is unique
            defaults=content_data
        )



def import_json_data_NM(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        # Create NewsContent instance
        content_data = Content.objects.create(
            content_source_id=4,
            content_source="NM",
            content_headline=news_item['headline'],
            content_url=news_item['url'],
            content_category=news_item['category'],
            content_text=news_item['content'][0]['data'],  # Assuming text is the first entry
            content_image=news_item['content'][1]['data'],  # Assuming image is the second entry
            content_date=news_item['published']
        )

        # Update or create the content instance
        Content.objects.update_or_create(
            content_headline=news_item['headline'],  # Assuming headline is unique
            defaults=content_data
        )

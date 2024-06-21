from rest_framework import serializers
from .models import Source, Category, Content, Thread, Snippet, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_id', 'option_default', 'option_added']


class SnippetSerializer(serializers.ModelSerializer):
    snippet_options = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ['snippet_id', 'snippet_text', 'time_to_consume', 'snippet_options']

    def get_snippet_options(self, obj):
        options = Option.objects.filter(snippet_id=obj.snippet_id)
        return OptionSerializer(options, many=True).data


class ThreadSerializer(serializers.ModelSerializer):
    news_snippet = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['thread_id', 'content_title', 'type', 'sentiment_valence', 'sentiment_arousal', 'style', 'tone',
                  'news_snippet']

    def get_news_snippet(self, obj):
        snippets = Snippet.objects.filter(thread_id=obj.thread_id)
        return SnippetSerializer(snippets, many=True).data


class ContentSerializer(serializers.ModelSerializer):
    news_thread = serializers.SerializerMethodField()
    content_category = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['content_id', 'content_headline', 'content_url', 'content_text', 'content_image', 'content_date',
                  'content_category', 'news_thread']

    def get_news_thread(self, obj):
        threads = Thread.objects.filter(content_id=obj.content_id)
        return ThreadSerializer(threads, many=True).data

    def get_content_category(self, obj):
        try:
            category = Category.objects.get(category_label=obj.content_category)
            return {
                "category_id": category.category_id,
                "category_label": category.category_label,
                "category_code": category.category_code
            }
        except Category.DoesNotExist:
            return None


class SourceSerializer(serializers.ModelSerializer):
    news_content = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = ['source_id', 'source_url', 'source_trust_rating', 'source_name', 'news_content']

    def get_news_content(self, obj):
        contents = Content.objects.filter(content_source_id=obj.source_id)
        return ContentSerializer(contents, many=True).data

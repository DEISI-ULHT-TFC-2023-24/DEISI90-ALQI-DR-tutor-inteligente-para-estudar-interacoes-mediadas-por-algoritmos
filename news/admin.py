from django.contrib import admin

from .models import Thread, Source, Content, Category, Option, Snippet

admin.site.register(Source)
admin.site.register(Thread)
admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(Snippet)
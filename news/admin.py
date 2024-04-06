from django.contrib import admin

from .models import Thread, Source, Content, Category

admin.site.register(Source)
admin.site.register(Thread)
admin.site.register(Content)
admin.site.register(Category)

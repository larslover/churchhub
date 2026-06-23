from django.contrib import admin
from .models import Topic, Series, Tag, Teaching, Resource

admin.site.register(Topic)
admin.site.register(Series)
admin.site.register(Tag)
admin.site.register(Teaching)
admin.site.register(Resource)
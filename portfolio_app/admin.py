from django.contrib import admin
from .models import Story, GalleryItem

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'published_date', 'read_time')
    list_filter = ('published_date', 'created_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)

class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('title',)
    date_hierarchy = 'created_date'

admin.site.register(Story, StoryAdmin)
admin.site.register(GalleryItem, GalleryItemAdmin)

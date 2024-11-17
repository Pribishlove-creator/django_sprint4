# Register your models here.
from django.contrib import admin
from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category',
        'location', 'is_published', 'pub_date', 'created_at'
    )
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('is_published', 'category', 'location')
    date_hierarchy = 'pub_date'
    autocomplete_fields = ('author', 'category', 'location')
    list_editable = ('is_published',)

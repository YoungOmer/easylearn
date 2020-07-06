from django.contrib import admin
from django.db import models
from .models import Blog, Category, Series

# Register your models here.

admin.site.register(Category)

@admin.register(Series)
class AdminSeries(admin.ModelAdmin):
    list_display = ['title','owner']


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display    =   ['author','view']
    list_filter     =   ['author',]
    list_per_page   =   50
    readonly_fields =   ['edited','date_stamp','time_edited']
    exclude         =   ['like','dislike','slug']




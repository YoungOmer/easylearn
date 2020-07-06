from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.shortcuts import reverse
from accounts.models import User
from django.utils import timezone
from mysite.utils import unique_slug_generator
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name        =   models.CharField(max_length=100)
    slug        =   models.SlugField(blank=True, unique=True)
    date_added  =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categoeris"
        

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})


class Series(models.Model):
    owner       =       models.ForeignKey(User, related_name="owner", null=True, on_delete=models.CASCADE)
    title       =       models.CharField(max_length=129)
    slug        =       models.SlugField(unique=True, blank=True)
    timestamp   =       models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "series"

    def get_absolute_url(self):
        return reverse('series_detail', kwargs={'slug':self.slug})



class Blog(models.Model):
    author      =   models.ForeignKey(User, on_delete=models.CASCADE)
    title       =   models.CharField(max_length=120)
    content     =   RichTextField()#config_name='special'
    view        =   models.PositiveIntegerField(default=0)
    image       =   models.ImageField(upload_to = "blog/%Y/%m/%d/", blank=True, null=True)
    category    =   models.ManyToManyField(Category, related_name="category")
    series      =   models.ManyToManyField(Series, blank=True, related_name="series")
    date_stamp  =   models.DateTimeField(auto_now_add=True)
    like        =   models.ManyToManyField(User, blank=True, related_name="like")
    dislike     =   models.ManyToManyField(User, blank=True, related_name="dislike")
    edited      =   models.BooleanField(default=False)
    time_edited =   models.DateTimeField(default=timezone.now)
    slug        =   models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering    =  ["-view",]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk':self.pk})

    # @property
    # def comments(self):
    #     instance = self
    #     qs = Comment.objects.filter_by_instance(instance)
    #     return qs

    # @property
    # def get_content_type(self):
    #     instance = self
    #     content_type = ContentType.objects.get_for_model(instance.__class__)
    #     return content_type



#### Generate Unique Slug
def slug_generator(sender, instance, *args, **kargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Series)
pre_save.connect(slug_generator, sender=Blog)
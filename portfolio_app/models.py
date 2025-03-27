from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Story(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    read_time = models.PositiveIntegerField(help_text="Estimated read time in minutes", default=5)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = "Stories"
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse('story_detail', args=[self.slug])
    
    def __str__(self):
        return self.title

class GalleryItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    created_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = "Gallery Items"
    
    def __str__(self):
        return self.title

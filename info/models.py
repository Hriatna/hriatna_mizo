
# Create your models here.
from django.db import models
from django.utils.text import slugify

class Info(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ExampleLanguage(models.Model):
    title = models.CharField(max_length=255,null=True)
    language = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.title

class Examples(models.Model):
    language = models.ForeignKey(ExampleLanguage,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255,null=True)
    body = models.TextField(blank=True)

    
    def __str__(self):
        return self.title 
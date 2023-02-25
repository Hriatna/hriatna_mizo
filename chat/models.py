from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    query=models.TextField(blank=True)
    translated_query=models.TextField(blank=True)
    query_timestamp = models.DateTimeField(null=True)
    original_response = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_timestamp = models.DateTimeField(null=True)
    final_language = models.CharField(max_length=10,null=True)
    language_confidence = models.FloatField(null=True,blank=True)
    created = models.IntegerField(null=True)
    duration = models.FloatField(null=True,blank=True)

    
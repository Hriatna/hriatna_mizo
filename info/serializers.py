from rest_framework import serializers
from .models import *

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'


class ExampleLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleLanguage
        fields = ['id', 'title', 'language']


class ExamplesSerializer(serializers.ModelSerializer):
    language = ExampleLanguageSerializer()

    class Meta:
        model = Examples
        fields = ['id', 'title', 'body', 'language']


from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        # fields='__all__'
        fields=['user','query','response','query_timestamp','response_timestamp']
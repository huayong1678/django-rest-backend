from http.client import responses
from rest_framework import serializers
from .models import Source
from users.models import User
from django.contrib.auth.hashers import make_password, check_password
# from cryptography.fernet import Fernet


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "host", "tag", "user", "port", "password", "database", "tablename", "engine"]
        extra_kwargs = {
            # 'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        owner_id = self.context["owner_id"]
        validated_data['owner'] = User.objects.get(id=owner_id)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
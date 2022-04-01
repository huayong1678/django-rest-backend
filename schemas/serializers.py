from http.client import responses
from rest_framework import serializers
from .models import DatabaseSchema
from users.models import User
from sources.models import Source
from dests.models import Dest


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseSchema
        fields = ["id", "tag", "dest", "source", "isSensitive"]
    
    def create(self, validated_data):
        owner_id = self.context["owner_id"]
        validated_data['owner'] = User.objects.get(id=owner_id)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
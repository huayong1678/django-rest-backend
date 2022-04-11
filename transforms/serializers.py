from http.client import responses
from rest_framework import serializers
from .models import Transform
from users.models import User
from django.contrib.auth.hashers import make_password, check_password


class TransformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transform
        # fields = []
        fields = ['id', 'uuid', 'owner']
        extra_kwargs = {
        }
    
    def create(self, validated_data):
        owner_id = self.context["owner_id"]
        uuid = self.context["uuid"]
        validated_data['uuid'] = uuid
        validated_data['owner'] = User.objects.get(id=owner_id)
        instance = self.Meta.model(**validated_data)
        # print(validated_data)
        instance.save()
        return instance

from http.client import responses
from rest_framework import serializers
from .models import Dest
from users.models import User
# from django.contrib.auth.hashers import make_password, check_password
# from cryptography.fernet import Fernet


class DestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dest
<<<<<<< HEAD
        fields = ["id", "host", "name", "user", "port", "password"]
=======
        fields = ["id", "host", "tag", "user", "port", "password", "database", "tablename", "engine"]
>>>>>>> origin/main
        extra_kwargs = {
            # 'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        owner_id = self.context["owner_id"]
        validated_data['owner'] = User.objects.get(id=owner_id)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
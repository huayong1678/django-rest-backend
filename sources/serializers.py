from http.client import responses
from rest_framework import serializers
from .models import Source
from users.models import User
from django.contrib.auth.hashers import make_password, check_password
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "host", "name", "user", "port", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # password = make_password(validated_data.pop('password', None))
        encrypt_pwd = make_password(validated_data['password'])
        validated_data['password'] = encrypt_pwd
        owner_id = self.context["owner_id"]
        validated_data['owner'] = User.objects.get(id=owner_id)
        # print("User:" + str(User.objects.get(id=owner_id)))
        # validated_data['owner'] = owner_id
        # print("S/P: " + str(owner_id))
        # print("S: " + str(validated_data['owner']))
        # print(encrypt_pwd)
        print("Validated:" + str(validated_data))
        instance = self.Meta.model(**validated_data)
        # print("Instance:" + str(instance))
        instance.save()
        return instance
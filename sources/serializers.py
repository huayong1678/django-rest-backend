from http.client import responses
from rest_framework import serializers
from .models import Source
from django.contrib.auth.hashers import make_password, check_password
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # password = make_password(validated_data.pop('password', None))
        encrypt_pwd = make_password(validated_data['password'])
        validated_data['password'] = encrypt_pwd
        # print(encrypt_pwd)
        # print(validated_data)
        instance = self.Meta.model(**validated_data)
        # print(instance)
        instance.save()
        return instance
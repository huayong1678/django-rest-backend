from http.client import responses
from rest_framework import serializers
from .models import Source
from django.contrib.auth.hashers import make_password, check_password
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': False}
        }
    
    def create(self, validated_data):
        # password = validated_data.pop('password', None)
        password = make_password(validated_data.pop('password', None))
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
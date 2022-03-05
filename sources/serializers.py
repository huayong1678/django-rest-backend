from http.client import responses
from rest_framework import serializers
from .models import Source
from users.models import User
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "host", "name", "user", "port", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # encrypt_pwd = make_password(validated_data['password'])
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypt_pwd = fernet.encrypt(validated_data['password'].encode())
        decrypt_pwd = fernet.decrypt(encrypt_pwd).decode()
        # print("Plaintext: " + str(validated_data['password']))
        # print("Encrypted: " + str(encrypt_pwd))
        # print("Decrypted: " + str(decrypt_pwd))
        validated_data['password'] = encrypt_pwd
        owner_id = self.context["owner_id"]
        validated_data['owner'] = User.objects.get(id=owner_id)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
from .models import Source
from .serializers import SourceSerializer
from logging import raiseExceptions
# from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
# from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404
# from django.http import JsonResponse
import jwt, datetime
# from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
import json
# from cryptography.fernet import Fernet

class CreateSource(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        serializer = SourceSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ListSource(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        source = Source.objects.filter(owner_id=payload['id'])
        serializer = SourceSerializer(source, many=True)

        return Response(serializer.data)

class DetailSource(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            source = Source.objects.filter(owner_id=payload['id']).get(pk=pk)
        except:
            raise Http404
        serializer = SourceSerializer(source)
        return Response(serializer.data)

class DeleteSource(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            if Source.objects.filter(pk=pk).exists():
                print(Source.objects.filter(pk=pk).exists())
                Source.objects.filter(owner_id=payload['id']).get(pk=pk).delete()
            else:
                raise Http404
        except:
            raise Http404
        return Response({"detail": "Deleted"})

class UpdateSource(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        # qs = Source.objects.prefetch_related('tracks')
        data = request.data
        qs = Source.objects.filter(owner_id=payload['id']).filter(pk=pk).first()
        serializer = SourceSerializer(qs, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
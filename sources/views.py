from rest_framework import generics
from .models import Source
from .serializers import SourceSerializer
from logging import raiseExceptions
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class ListSource(generics.ListCreateAPIView):
    def get(self, request):
        queryset = Source.objects.all()
        serializer_class = SourceSerializer
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        source = Source.objects.all()
        serializer = SourceSerializer(source)
        return Response(serializer.data)

class DetailSource(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request):
        queryset = Source.objects.all()
        serializer_class = SourceSerializer
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        source = Source.objects.all()
        serializer = SourceSerializer(source)
        return Response(serializer.data)

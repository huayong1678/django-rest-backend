from .models import Source
from .serializers import SourceSerializer
from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
import datetime
from rest_framework.decorators import api_view
import json
from jwt_authentication.jwtAuth import *


class CreateSource(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        serializer = SourceSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListSource(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        source = Source.objects.filter(owner_id=payload['id'])
        serializer = SourceSerializer(source, many=True)
        return Response(serializer.data)


class DetailSource(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            source = Source.objects.filter(owner_id=payload['id']).get(pk=pk)
        except:
            raise Http404
        serializer = SourceSerializer(source)
        return Response(serializer.data)


class DeleteSource(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            if Source.objects.filter(pk=pk).exists():
                print(Source.objects.filter(pk=pk).exists())
                Source.objects.filter(
                    owner_id=payload['id']).get(pk=pk).delete()
            else:
                raise Http404
        except:
            raise Http404
        return Response({"detail": "Deleted"})


class UpdateSource(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        data = request.data
        qs = Source.objects.filter(
            owner_id=payload['id']).filter(pk=pk).first()
        serializer = SourceSerializer(qs, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

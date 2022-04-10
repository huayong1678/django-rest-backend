from .models import Dest
from .serializers import DestSerializer
from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
import jwt, datetime
import json
from jwt_authentication.jwtAuth import *

class CreateDest(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        serializer = DestSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ListDest(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        dest = Dest.objects.filter(owner_id=payload['id'])
        serializer = DestSerializer(dest, many=True)

        return Response(serializer.data)

class DetailDest(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            dest = Dest.objects.filter(owner_id=payload['id']).get(pk=pk)
        except:
            raise Http404
        serializer = DestSerializer(dest)
        return Response(serializer.data)

class DeleteDest(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            if Dest.objects.filter(pk=pk).exists():
                print(Dest.objects.filter(pk=pk).exists())
                Dest.objects.filter(owner_id=payload['id']).get(pk=pk).delete()
            else:
                raise Http404
        except:
            raise Http404
        return Response({"detail": "Deleted"})

class UpdateDest(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        data = request.data
        qs = Dest.objects.filter(owner_id=payload['id']).filter(pk=pk).first()
        serializer = DestSerializer(qs, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
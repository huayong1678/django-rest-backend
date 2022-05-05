from .models import Transform
from .serializers import TransformSerializer
from django.shortcuts import render
from logging import raiseExceptions
import datetime
import json
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from db_handler.dynamoDB import *
from jwt_authentication.jwtAuth import *

class DynamoCheckView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        status = dynamoCheck()
        return Response(status)


class CreateTransformView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        data = request.data
        response = dynamoCreateTransform(data, payload)
        request.data['owner'] = payload['id']
        request.data['uuid'] = response['UUID']
        serializer = TransformSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.context['uuid'] = response['UUID']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"HTTPStatusCode": response['HTTPStatusCode'], "uuid": response['UUID']})

class DeleteTransformView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            transform = Transform.objects.filter(owner_id=payload['id']).get(pk=pk)
        except:
            raise Http404
        serializer = TransformSerializer(transform)
        try:
            response = dynamoGetTransform(serializer.data)
        except:
            raise Http404
        return Response(response)

class ListTransformView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        transform = Transform.objects.filter(owner_id=payload['id'])
        serializer = TransformSerializer(transform, many=True)
        return Response(serializer.data)

class GetTransformView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            transform = Transform.objects.filter(owner_id=payload['id']).get(pk=pk)
        except:
            raise Http404
        serializer = TransformSerializer(transform)
        response = dynamoGetTransform(serializer.data)
        return Response(response)

class UpdateTransformView(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            transform = Transform.objects.filter(owner_id=payload['id']).get(pk=pk)
            serializer = TransformSerializer(transform)
        except:
            raise Http404
        response = dynamoUpdateTransform(request.data, payload, serializer.data['uuid'], serializer.data['id'])
        return Response(response)
        # return Response({"HTTPStatusCode": response['HTTPStatusCode'], "uuid": response['UUID']})
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


class TestView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        return Response(payload)

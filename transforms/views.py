from django.shortcuts import render
import jwt
import datetime
import json
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
# from db_handler.dbConnect import *
# from db_handler.dbInfo import *
# from db_handler.dbTable import *
from db_handler.dynamoDB import *


class DynamoCheckView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        status = dynamoCheck()
        return Response(status)

class CreateTransformView(APIView):
  def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        data = request.data
        dynamoCheck()
        response = dynamoCreateTransform(data, payload)
        return Response(response)

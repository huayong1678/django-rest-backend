from .models import Source
from .serializers import SourceSerializer
from logging import raiseExceptions
# from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404
import jwt, datetime
from django.contrib.auth.hashers import make_password, check_password

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
        print(serializer.data)
        return Response(serializer.data)

class DeleteSource(APIView):
    pass
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DatabaseSchema
from sources.models import Source
from dests.models import Dest
from .serializers import SchemaSerializer
from sources.serializers import SourceSerializer
from dests.serializers import DestSerializer
from logging import raiseExceptions
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Methods Views

class CreateSchemaView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        serializer = SchemaSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ListSchemaView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        schema = DatabaseSchema.objects.filter(owner_id=payload['id'])
        serializer = SchemaSerializer(schema, many=True)

        return Response(serializer.data)

class DetailSchemaView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            schema = DatabaseSchema.objects.filter(owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            source = Source.objects.filter(owner_id=payload['id']).get(pk=schema_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(pk=schema_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
        except:
            Http404
        data = {"schema_id": schema_serializer.data['id'], 
        "schema_tag": schema_serializer.data['tag'],
        "source": {"tag": source_serializer.data['tag'],
        "host": source_serializer.data['host']},  
        "dest": {"tag": dest_serializer.data['tag'],
        "host": dest_serializer.data['host']}}
        return Response(data)

class DeleteSchemaView(APIView):
    def post(self, request, pk):
        return Response({"detail": "pass"})

class UpdateSchemaView(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        data = request.data
        qs = DatabaseSchema.objects.filter(owner_id=payload['id']).filter(pk=pk).first()
        serializer = SchemaSerializer(qs, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# DB Handler

class SchemaView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            schema = DatabaseSchema.objects.filter(owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            source = Source.objects.filter(owner_id=payload['id']).get(pk=schema_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(pk=schema_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            database = source_serializer.data['database']
            user = source_serializer.data['user']
            password = source_serializer.data['password']
            host = source_serializer.data['host']
            connection_string = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
            alchemyEngine   = create_engine(connection_string, pool_recycle=3600);
            dbConnection    = alchemyEngine.connect();
            dataFrame       = pd.read_sql("select * from \"actor\"", dbConnection);
            pd.set_option('display.expand_frame_repr', False);
            dbConnection.close();
        except:
            raise Http404
        return Response(dataFrame.head(10))

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
import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
# import psycopg2
# import pandas as pd
# from sqlalchemy import create_engine
from schemas.db_connection.dbConnection import *

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
            schema = DatabaseSchema.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            data = {"schema_id": schema_serializer.data['id'],
                    "schema_tag": schema_serializer.data['tag'],
                    "isSensitive": schema_serializer.data['isSensitive'],
                    "source": {"tag": source_serializer.data['tag'],
                               "host": source_serializer.data['host']},
                    "dest": {"tag": dest_serializer.data['tag'],
                             "host": dest_serializer.data['host']}}
            response = data
        except:
            response = {"detail": "No object."}
        return Response(response)


class DeleteSchemaView(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        data = request.data
        try:
          qs = DatabaseSchema.objects.filter(owner_id=payload['id']).filter(pk=pk).first()
          qs.delete()
          response = {"detail": "Object deleted."}
        except:
          response = {"detail": "No Object."}
        return Response(response)


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
        qs = DatabaseSchema.objects.filter(
            owner_id=payload['id']).filter(pk=pk).first()
        serializer = SchemaSerializer(qs, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# DB Handler


class SourceSchemaView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            schema = DatabaseSchema.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            database = source_serializer.data['database']
            db_engine = source_serializer.data['engine']
            user = source_serializer.data['user']
            password = source_serializer.data['password']
            host = source_serializer.data['host']
            table = source_serializer.data['tablename']
            isSensitive = schema_serializer.data['isSensitive']
            connection_data = [db_engine, user, password,
                            host, database, isSensitive, table]
            connection = testConnection(connection_data)
            head = showData(connection_data)
            response = {"status": "Connection Success" if connection == True else "Connection Failed", "data": head}
        except:
            response = {"status": "No object."}
        return Response(response)


class DestSchemaView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            schema = DatabaseSchema.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            dest = Dest.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            database = dest_serializer.data['database']
            db_engine = dest_serializer.data['engine']
            user = dest_serializer.data['user']
            password = dest_serializer.data['password']
            host = dest_serializer.data['host']
            table = dest_serializer.data['tablename']
            isSensitive = schema_serializer.data['isSensitive']
            connection_data = [db_engine, user, password,
                            host, database, isSensitive, table]
            print(connection_data)
            connection = testConnection(connection_data)
            head = showData(connection_data)
            response = {"status": "Connection Success" if connection == True else "Connection Failed", "data": head}
        except:
            response = {"status": "No object."}
        return Response(response)


class DBConnectionView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            schema = DatabaseSchema.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            schema_serializer = SchemaSerializer(schema)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(
                pk=schema_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            source_database, dest_database = source_serializer.data['database'], dest_serializer.data['database']
            source_db_engine, dest_db_engine = source_serializer.data['engine'], dest_serializer.data['engine']
            source_user, dest_user = source_serializer.data['user'], dest_serializer.data['user']
            source_password, dest_password = source_serializer.data['password'], dest_serializer.data['password']
            source_host, dest_host = source_serializer.data['host'], dest_serializer.data['host']
            source_connection_data = [source_db_engine, source_user, source_password, source_host, source_database]
            dest_connection_data = [source_db_engine, source_user, source_password, source_host, source_database]
            source_connection = testConnection(source_connection_data)
            dest_connection = testConnection(dest_connection_data)
            source_status = "Connection Success" if source_connection == True else "Unable to connect."
            dest_status = "Connection Success" if dest_connection == True else "Unable to connect."
            response = {"source": source_status, "dest": dest_status}
        except:
            response = "Unable to connect."
        return Response(response)

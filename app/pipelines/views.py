from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pipeline
from sources.models import Source
from dests.models import Dest
from .serializers import PipelineSerializer
from sources.serializers import SourceSerializer
from dests.serializers import DestSerializer
from logging import raiseExceptions
import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
from db_handler.dbConnect import *
from db_handler.dbInfo import *
from db_handler.dbTable import *
from jwt_authentication.jwtAuth import *

# Methods Views


class CreatePipelineView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        serializer = PipelineSerializer(data=request.data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListPipelineView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        pipeline = Pipeline.objects.filter(owner_id=payload['id'])
        serializer = PipelineSerializer(pipeline, many=True)
        return Response(serializer.data)


class DetailPipelineView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            pipeline_serializer = PipelineSerializer(pipeline)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=pipeline_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(
                pk=pipeline_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            data = {"pipeline_id": pipeline_serializer.data['id'],
                    "pipeline_tag": pipeline_serializer.data['tag'],
                    "isSensitive": pipeline_serializer.data['isSensitive'],
                    "source": {"tag": source_serializer.data['tag'],
                               "host": source_serializer.data['host']},
                    "dest": {"tag": dest_serializer.data['tag'],
                             "host": dest_serializer.data['host']}}
            response = data
        except:
            response = {"detail": "No object."}
        return Response(response)


class DeletePipelineView(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        data = request.data
        try:
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).filter(pk=pk).first()
            pipeline.delete()
            response = {"detail": "Object deleted."}
        except:
            response = {"detail": "No Object."}
        return Response(response)


class UpdatePipelineView(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        data = request.data
        pipeline = Pipeline.objects.filter(
            owner_id=payload['id']).filter(pk=pk).first()
        serializer = PipelineSerializer(pipeline, data=data)
        serializer.context['owner_id'] = payload['id']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# DB Handler


class SourcePipelineView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        pipeline = Pipeline.objects.filter(
            owner_id=payload['id']).get(pk=pk)
        pipeline_serializer = PipelineSerializer(pipeline)
        source = Source.objects.filter(owner_id=payload['id']).get(
            pk=pipeline_serializer.data['source'])
        source_serializer = SourceSerializer(source)
        database = source_serializer.data['database']
        db_engine = source_serializer.data['engine']
        user = source_serializer.data['user']
        password = source_serializer.data['password']
        host = source_serializer.data['host']
        table = source_serializer.data['tablename']
        port = source_serializer.data['port']
        isSensitive = pipeline_serializer.data['isSensitive']
        connection_data = [db_engine, user, password,
                           host, database, isSensitive, table, port]
        connection = testConnection(connection_data)
        head = showData(connection_data)
        response = {"data" if connection == True else "error": head}
        return Response(response)


class DestPipelineView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        pipeline = Pipeline.objects.filter(
            owner_id=payload['id']).get(pk=pk)
        pipeline_serializer = PipelineSerializer(pipeline)
        dest = Dest.objects.filter(owner_id=payload['id']).get(
            pk=pipeline_serializer.data['dest'])
        dest_serializer = DestSerializer(dest)
        database = dest_serializer.data['database']
        db_engine = dest_serializer.data['engine']
        user = dest_serializer.data['user']
        password = dest_serializer.data['password']
        host = dest_serializer.data['host']
        table = dest_serializer.data['tablename']
        port = dest_serializer.data['port']
        isSensitive = pipeline_serializer.data['isSensitive']
        connection_data = [db_engine, user, password,
                           host, database, isSensitive, table, port]
        connection = testConnection(connection_data)
        head = showData(connection_data)
        response = {"data" if connection != True else "database_error": head}
        return Response(response)


class DBConnectionView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).get(pk=pk)
            pipeline_serializer = PipelineSerializer(pipeline)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=pipeline_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            dest = Dest.objects.filter(owner_id=payload['id']).get(
                pk=pipeline_serializer.data['dest'])
            dest_serializer = DestSerializer(dest)
            source_database, dest_database = source_serializer.data[
                'database'], dest_serializer.data['database']
            source_db_engine, dest_db_engine = source_serializer.data[
                'engine'], dest_serializer.data['engine']
            source_user, dest_user = source_serializer.data['user'], dest_serializer.data['user']
            source_password, dest_password = source_serializer.data[
                'password'], dest_serializer.data['password']
            source_host, dest_host = source_serializer.data['host'], dest_serializer.data['host']
            source_connection_data = [
                source_db_engine, source_user, source_password, source_host, source_database]
            dest_connection_data = [
                dest_db_engine, dest_user, dest_password, dest_host, dest_database]
            source_connection = testConnection(source_connection_data)
            dest_connection = testConnection(dest_connection_data)
            source_status = "Connection Success" if source_connection == True else "Unable to connect."
            dest_status = "Connection Success" if dest_connection == True else "Unable to connect."
            response = {"source": source_status, "dest": dest_status}
        except:
            response = "Unable to connect."
        return Response(response)

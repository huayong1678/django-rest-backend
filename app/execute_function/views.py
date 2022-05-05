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
from db_handler.dynamoDB import *
from db_handler.dbTable import *
from database_migration.dms import *
from transforms.serializers import TransformSerializer
from transforms.models import Transform
from pipelines.serializers import PipelineSerializer
from pipelines.models import Pipeline
from dests.serializers import DestSerializer
from dests.models import Dest
from sources.serializers import SourceSerializer
from sources.models import Source
from django.http import HttpResponseServerError


class PrepareTableView(APIView):
    def get(self, request, pipeline_pk, transform_pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            transform = Transform.objects.filter(
                owner_id=payload['id']).get(pk=transform_pk)
            transform_serializer = TransformSerializer(transform)
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).get(pk=pipeline_pk)
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
            isSensitive = pipeline_serializer.data['isSensitive']
            connection_data = [db_engine, user, password,
                               host, database, isSensitive, table]
            dynamo_response = dynamoGetTransform(transform_serializer.data)
            schema = getSchema(connection_data)
            head = showData(connection_data)
        except:
            raise Http404
        # transform_data = {
        #     "schemas": dynamo_response['Item']['SCHEMAS'], "scripts": dynamo_response['Item']['SCRIPTS']}
        transform_data = {
            "schemas": dynamo_response['Item']['SCHEMAS']}
        dest_data = {"schemas": schema if schema != table else "unavailable"}
        response = {"detail": "available" if checkTable(connection_data) else "no such table", "table_schema" if schema !=
                    table else "required_table": schema, "transform_data": transform_data, "dest_data": dest_data}
        return Response(response)


class ApplyTableView(APIView):
    def post(self, request, pipeline_pk, transform_pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            transform = Transform.objects.filter(
                owner_id=payload['id']).get(pk=transform_pk)
            transform_serializer = TransformSerializer(transform)
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).get(pk=pipeline_pk)
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
            isSensitive = pipeline_serializer.data['isSensitive']
            connection_data = [db_engine, user, password,
                               host, database, isSensitive, table]
            try:
                dynamo_response = dynamoGetTransform(transform_serializer.data)
                if request.data['create_table']:
                    create_status = createTable(connection_data,
                                                dynamo_response['Item']['SCHEMAS'], request.data['pk'])
                    table_status = checkTable(connection_data)
                    response = {"table_name": table, "schemas_to_apply": dynamo_response['Item']['SCHEMAS'], "detail": create_status}
                else:
                    response = {
                        "detail": "Execution Cancled. Any change will not apply."}
            except:
                return HttpResponseServerError()
        except:
            raise Http404
        return Response(response)


class ApplyMigrateView(APIView):
    def get(self, request, pipeline_pk, transform_pk):
        token = request.COOKIES.get('jwt')
        payload = isAuthen(token)
        try:
            pipeline = Pipeline.objects.filter(
                owner_id=payload['id']).get(pk=pipeline_pk)
            pipeline_serializer = PipelineSerializer(pipeline)
            source = Source.objects.filter(owner_id=payload['id']).get(
                pk=pipeline_serializer.data['source'])
            source_serializer = SourceSerializer(source)
            transform = Transform.objects.filter(
                owner_id=payload['id']).get(pk=transform_pk)
            transform_serializer = TransformSerializer(transform)
            database = source_serializer.data['database']
            db_engine = source_serializer.data['engine']
            user = source_serializer.data['user']
            password = source_serializer.data['password']
            host = source_serializer.data['host']
            table = source_serializer.data['tablename']
            port = source_serializer.data['port']
            connection_data = [db_engine, user, password,
                            host, port, database, table]
            try:
                response = dynamoGetTransform(transform_serializer.data)
                tmp = exportData(connection_data, payload['id'], response)
                importData(tmp, response)
                removeLocalData(tmp[1])
            except:
                return HttpResponseServerError()
        except:
            raise Http404
        return Response(response['Item'])

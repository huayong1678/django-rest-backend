from django.urls import path, include
from .views import CreateSchemaView, ListSchemaView, DeleteSchemaView, UpdateSchemaView, DetailSchemaView, SourceSchemaView, DestSchemaView, DBConnectionView

urlpatterns = [
    path('create', CreateSchemaView.as_view()),
    path('list', ListSchemaView.as_view()),
    path('detail/<int:pk>', DetailSchemaView.as_view()),
    path('delete/<int:pk>', DeleteSchemaView.as_view()),
    path('update/<int:pk>', UpdateSchemaView.as_view()),
    path('source/<int:pk>', SourceSchemaView.as_view()),
    path('dest/<int:pk>', DestSchemaView.as_view()),
    path('test/<int:pk>', DBConnectionView.as_view()),
]
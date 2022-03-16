from django.urls import path, include
from .views import CreateSchemaView, ListSchemaView, DeleteSchemaView, UpdateSchemaView, DetailSchemaView, SchemaView

urlpatterns = [
    path('create', CreateSchemaView.as_view()),
    path('list', ListSchemaView.as_view()),
    path('detail/<int:pk>', DetailSchemaView.as_view()),
    path('delete/<int:pk>', DeleteSchemaView.as_view()),
    path('update/<int:pk>', UpdateSchemaView.as_view()),
    path('<int:pk>', SchemaView.as_view()),
]
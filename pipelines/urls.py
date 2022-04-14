from django.urls import path, include
from .views import *

urlpatterns = [
    path('create', CreatePipelineView.as_view()),
    path('list', ListPipelineView.as_view()),
    path('detail/<int:pk>', DetailPipelineView.as_view()),
    path('delete/<int:pk>', DeletePipelineView.as_view()),
    path('update/<int:pk>', UpdatePipelineView.as_view()),
    path('source/<int:pk>', SourcePipelineView.as_view()),
    path('dest/<int:pk>', DestPipelineView.as_view()),
    path('connection/<int:pk>', DBConnectionView.as_view()),
]
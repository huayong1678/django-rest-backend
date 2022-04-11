from django.urls import path, include
from .views import *

urlpatterns = [
    path('prepare-table/<int:pipeline_pk>/<int:transform_pk>', PrepareTableView.as_view()),
    path('apply-table/<int:pipeline_pk>/<int:transform_pk>', ApplyTableView.as_view()),
]
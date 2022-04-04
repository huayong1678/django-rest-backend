from django.urls import path, include
from .views import *

urlpatterns = [
    # path('dynamodb', DynamoCheckView.as_view()),
    path('create', CreateTransformView.as_view()),
]
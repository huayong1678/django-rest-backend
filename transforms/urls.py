from django.urls import path, include
from .views import *

urlpatterns = [
    # path('dynamodb', DynamoCheckView.as_view()),
    path('create', CreateTransformView.as_view()),
    path('list', ListTransformView.as_view()),
    path('<int:pk>', GetTransformView.as_view()),
    path('delete/<int:pk>', DeleteTransformView.as_view()),
]
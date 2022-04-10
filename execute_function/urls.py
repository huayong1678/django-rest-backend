from django.urls import path, include
from .views import *

urlpatterns = [
    path('', TestView.as_view()),
]
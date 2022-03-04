from django.urls import path
from .views import ListSource, DetailSource, CreateSource

urlpatterns = [
    path('list', ListSource.as_view()),
    path('<int:pk>', DetailSource.as_view()),
    path('create', CreateSource.as_view()),
]
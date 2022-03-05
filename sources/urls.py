from django.urls import path
from .views import ListSource, DetailSource, CreateSource, DeleteSource

urlpatterns = [
    path('list', ListSource.as_view()),
    path('detail/<int:pk>', DetailSource.as_view()),
    path('create', CreateSource.as_view()),
    path('delete', DeleteSource.as_view()),
]